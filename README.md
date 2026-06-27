# TNAgriculturalChatBot
# 🌾 Tamil Nadu Agriculture Welfare Scheme Bot

An AI-powered Retrieval-Augmented Generation (RAG) application built with **LangChain**, **FAISS**, and **Streamlit**. It fetches, splits, embeds, and queries information directly from the official Tamil Nadu Government Welfare Scheme Portal for the Agriculture - Farmers Welfare Department.

---

## 📐 Overall System Flow

[ Webpage URL ]
│
▼ (Step 1: WebBaseLoader)
[ Raw HTML / Text Data ]
│
▼ (Step 2: RecursiveCharacterTextSplitter)
[ Document Chunks (Size: 1000, Overlap: 150) ]
│
▼ (Step 3: OpenAIEmbeddings)
[ Vector Representations ] ────> Stored in ────> [ FAISS Vector DB ]
│
▼ (Step 4)
[ User Query ] ───> Searches Closest Chunks ───> [ Context Extracted ]
│
▼ (Step 5)
[ Prompt Template ] + [ Context ] ───> [ GPT-4o-Mini ] ───> [ Streamlit Chat UI ]

---

## 🚀 Features

* **Live Data Ingestion:** Scrapes live scheme data directly from the TN Government portal.
* **Smart Chunking:** Employs recursive character text splitting to maintain contextual sentences.
* **Blazing Fast Retrieval:** Uses a highly-optimized local FAISS vector database for semantic similarity matching.
* **Persistent Interface:** Built with a interactive Streamlit UI using session caching to avoid unnecessary website scraping.

---

## 🛠️ Installation & Setup

### 1. Clone or Open the Project Directory
Navigate to your project root folder where `app.py` resides.

### 2. Configure Environment Variables
Create a `.env` file in the root directory and add your OpenAI API key:
```env
OPENAI_API_KEY=your_actual_openai_api_key_here

3. Install Dependencies
Run the following command to install all the necessary packages inside your virtual environment (venv):

Bash
pip install streamlit langchain langchain-community langchain-core langchain-openai faiss-cpu beautifulsoup4 python-dotenv

How to Run the Application
Launch the frontend dashboard by running:

Bash
streamlit run app.py
Open http://localhost:8501 in your web browser to start asking questions about farming schemes, subsidies, and training programs!
