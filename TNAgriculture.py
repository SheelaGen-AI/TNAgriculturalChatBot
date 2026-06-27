import os
import streamlit as st
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
os.environ["USER_AGENT"] = "MyTNWelfareApp/1.0"

from langchain_community.document_loaders import WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

# --- STREAMLIT UI SETUP ---
st.set_page_config(page_title="TN Agri-Welfare Bot", page_icon="🌾")
st.title("🌾 Tamil Nadu Agriculture Scheme Assistant")
st.write("Ask questions about the Agriculture - Farmers Welfare Department schemes.")

# --- CACHE THE RAG CHAIN ---
# This prevents Streamlit from rebuilding the DB on every user click
if "rag_chain" not in st.session_state:
    with st.spinner("Loading TN Portal schemes & building database... Please wait."):
        # 1. Load
        url = "https://www.tn.gov.in/scheme_list.php?dep_id=Mg=="
        loader = WebBaseLoader(url)
        docs = loader.load()
        
        # 2. Split
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)
        chunks = text_splitter.split_documents(docs)
        
        # 3. Vector DB
        embeddings = OpenAIEmbeddings()
        db = FAISS.from_documents(chunks, embeddings)
        retriever = db.as_retriever(search_kwargs={"k": 2})
        
        # 4. LLM & Chain
        llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
        system_prompt = (
            "You are a helpful assistant for the Tamil Nadu Welfare Portal.\n"
            "Answer the user's question using ONLY the provided context below. "
            "If you do not know the answer based on the context, say 'I cannot find that information on the page.'\n\n"
            "Context:\n{context}"
        )
        prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("human", "{question}"),
        ])
        
        def format_docs(docs):
            return "\n\n".join(doc.page_content for doc in docs)
            
        # Build final chain
        chain = (
            {"context": retriever | format_docs, "question": RunnablePassthrough()}
            | prompt
            | llm
            | StrOutputParser()
        )
        
        # Save chain to session state
        st.session_state.rag_chain = chain
    st.success("Database ready!")

# --- CHAT HISTORY TRACKING ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages from history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- USER INPUT & RAG INVOCATION ---
if user_query := st.chat_input("Ask me about training, subsidies, or farming schemes..."):
    # Display user message
    st.chat_message("user").markdown(user_query)
    st.session_state.messages.append({"role": "user", "content": user_query})
    
    # Generate RAG response
    with st.chat_message("assistant"):
        with st.spinner("Searching schemes..."):
            response = st.session_state.rag_chain.invoke(user_query)
            st.markdown(response)
            
    # Save assistant response to history
    st.session_state.messages.append({"role": "assistant", "content": response})