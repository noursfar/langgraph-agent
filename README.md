# 🧠 llm-agent-lab

**LLM Agent Lab** is a production-ready AI agent built with **LangGraph** that autonomously decides when to call backend APIs and search through document knowledge bases. The agent integrates **RAG (Retrieval-Augmented Generation)** for medical document search, OAuth authentication for healthcare APIs, and structured tool calling.

---

## 🚀 Project Overview

This project demonstrates:
* Building an **LLM agent with LangGraph** that interprets user queries and executes tools dynamically
* **RAG pipeline** for semantic search across documents 
* **Custom tool integration** with precise descriptions and parameter schemas
* **OAuth2 authentication** for secure API access
* **Conversation memory** for multi-turn interactions
* Structured logging and error handling

---

## 🧩 Key Features

| Feature | Description                                                                                           |
|---------|-------------------------------------------------------------------------------------------------------|
| **LangGraph Agent** | Modern state-based agent with custom workflow control                                                 |
| **RAG System** | Document ingestion, embedding, and semantic search with ChromaDB                                      |
| **Tools** | `get_patient_data`, `get_pds_contact`, `retrieve_admin_info` |
| **OAuth Manager** | Async token retrieval and caching for API authentication                                              |
| **Token-based Chunking** | Uses tiktoken for precise token-level document splitting                                              |
| **OpenAI Embeddings** | text-embedding-ada-002 for high-quality semantic search                                               |
| **Conversation Memory** | SQL-based persistent conversation history across sessions                                              |
| **CLI Interface** | Interactive chat interface with session management                                                    |
| **REST API** | Flask-based REST API with OpenAPI documentation                                                       |
| **Session Management** | UUID-based session tracking for multi-user support                                                  |

---

## 🧱 Project Structure

```
llm-agent-lab/
│
├── Pipfile                      # Dependencies
├── main.py                      # Interactive CLI interface
├── app.py                       # Flask REST API server
├── README.md
│
├── api/                         # REST API implementation
│   ├── routes/
│   │   ├── chat.py             # Chat endpoint handlers
│   │   └── initialize.py        # Session initialization
│   ├── schemas/
│   │   ├── requests.py         # Request validation schemas
│   │   └── responses.py        # Response schemas
│   └── utils/
│       └── agent_store.py      # Session management
│
├── agent_core/
│   ├── __init__.py
│   │
│   ├── config/
│   │   └── settings.py          # Environment configuration
│   │
│   ├── utils/
│   │   ├── logger.py            # Centralized logging
│   │   ├── exceptions.py        # Custom exceptions
│   │   └── oauth.py             # OAuth2 token manager
│   │
│   ├── tools/
│   │   ├── get_patient_data.py  # Fetch patient information
│   │   ├── get_pds_contact.py   # Fetch healthcare professional contacts
│   │   └── rag_search.py        # Search medical documents (RAG)
│   │
│   ├── agent/
│   │   ├── base_agent.py        # LangGraph agent definition
│   │   └── executor.py          # Agent execution logic
│   │
│   └── rag/                     # RAG backend
│       ├── config.py            # RAG-specific configuration
│       ├── vector_store.py      # ChromaDB interface
│       └── ingest.py            # Document processing pipeline
│
├── scripts/                     # CLI for testing 
│   ├── reset_vector_db.py
│   ├── inspect_vs.py
│   └── ingest_docs.py           
│
└── data/
    ├── documents/               # Source documents
    └── chroma_db/               # ChromaDB vector store
```

---

## ⚙️ Setup Instructions

### 1. Clone the repository

```bash
git clone git@gitlab.com:your-org/llm-agent-lab.git
cd llm-agent-lab
```

### 2. Setup environment

```bash
pip install pipenv
pipenv install
pipenv shell
```

### 3. Environment variables (`.env`)

```bash
cp .env.example .env
```

---

## 📚 RAG Setup

### 1. Add documents to ingest

Place your medical documents in `data/documents/`:

### 2. Ingest documents

```bash
python -m scripts.ingest_docs data/documents/livretaccueilpatient.pdf
```

This will:
- Load the document using LangChain loaders
- Split into chunks using `TokenTextSplitter` (tiktoken)
- Generate embeddings with OpenAI `text-embedding-ada-002`
- Store in ChromaDB at `data/chroma_db/`

---

## 🧠 Running the Agent

### REST API Mode

```bash
pipenv run app
```

The server will start at `http://localhost:5000` with the following endpoints:

#### 1. Initialize Session
- **Endpoint**: `POST /api/v1/pds/initialize`
- **Description**: Creates a new conversation session
- **Request Body**:
  ```json
  {
    "userId": "user_123",
    "token": "your_auth_token"
  }
  ```

#### 2. Chat
- **Endpoint**: `POST /api/v1/pds/chat/<session_id>`
- **Description**: Send a message to the agent
- **Request Body**:
  ```json
  {
    "message": "Quels sont les protocoles d'admission?"
  }
  ```

API documentation is available at `/swagger-ui`.

### Interactive mode (CLI)

```bash
pipenv run main
```
🧠 LLM Agent Lab - LangGraph Agent Starting...

Enter your query (or 'quit' to exit): Quels sont les protocoles d'admission?

🤖 Agent Output:
Selon le livret d'accueil patient, les protocoles d'admission incluent...


### How the agent works:

1. **User query** → Agent analyzes intent
2. **Tool selection** → Agent decides which tool(s) to use:
   - `get_patient_data` - for patient information
   - `get_pds_contact` - for staff contacts
   - `search_documents` - for medical protocols
3. **Tool execution** → Fetches data from APIs or searches documents
4. **Response generation** → Synthesizes results into natural language


---

## 🧭 Development Roadmap
| Phase | Description | Status |
|-------|------------|--------|
| **1** | Project setup + config/logging | ✅ Done |
| **2** | Implement healthcare API tools | ✅ Done |
| **3** | Migrate to LangGraph | ✅ Done |
| **4** | Add OAuth Manager | ✅ Done |
| **5** | RAG pipeline with ChromaDB | ✅ Done |
| **6** | Multi-turn conversation memory | ✅ Done |
| **7** | Document ingestion CLI | ✅ Done |
| **8** | Prompting | ✅ Done |
| **9** | Agent personalization (context injection) | ✅ Done |
| **10** | REST API with Flask | ✅ Done |
| **11** | Conversation persistence (PostgreSQL) | ✅ Done |
| **12** | Integration tests & CI/CD | 🔜 Planned |
| **13** | API Documentation & Swagger UI | ✅ Done |
| **14** | Session Management & Multi-user Support | ✅ Done |

