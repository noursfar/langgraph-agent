# 🧠 llm-agent-lab

**LLM Agent Lab** is a lightweight proof-of-concept project demonstrating how to build an **LLM-powered agent** that can autonomously decide when to call backend APIs via registered tools.
This version uses the **LangChain Agent** framework (before migrating to LangGraph), with integrated logging, configuration management, and OAuth authentication.

---

## 🚀 Project Overview

This project explores how to:

* Build an **LLM agent** that interprets user queries and calls backend APIs dynamically.
* Integrate **custom Python tools** with precise descriptions and parameter schemas.
* Log and trace agent reasoning for debugging and monitoring.

---

## 🧩 Current Features

| Feature                | Description                                           |
| ---------------------- | ----------------------------------------------------- |
| **Agent Architecture** | Modular structure using `agent_core` package          |
| **Tool Integration**   | Supports async tools registered via `@tool` decorator |
| **Example Tool**       | `get_pds_contact` – fetches professional contact info |
| **OAuth Manager**      | Handles token retrieval and caching for API access    |
| **Config System**      | Pydantic `BaseSettings` for environment variables     |
| **Logger**             | Centralized logger with configurable log levels       |
| **CLI Entry**          | Test the agent via terminal with user queries         |

---

## 🧱 Project Structure

```
llm-agent-lab/
│
├── Pipfile                  # Environment + dependencies
├── main.py                  # CLI entrypoint for testing
│
└── agent_core/
    ├── __init__.py
    │
    ├── config/
    │   ├── settings.py       # Pydantic-based settings
    │
    ├── utils/
    │   ├── logger.py         # Centralized logging config
    │   ├── exceptions.py     # Custom exceptions
    │   └── oauth_manager.py  # Async OAuth2 token manager
    │
    ├── tools/
    │   ├── get_pds_contact.py # Example LangChain tool
    │
    ├── agent/
    │   ├── base_agent.py     # Agent creation logic
    │   └── executor.py       # CLI execution and error handling
    │
    └── __main__.py           # Optional entry point
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
# Copy example environment file
cp .env.example .env

# Edit with your credentials
nano .env
```

---

## 🧠 Running the Agent

### Interactive mode (CLI)

```bash
pipenv run main
```

Example:

```
Enter your query: chercher adem daami
```

Agent output:

```
[INFO] Running agent with user input: chercher adem daami
[INFO] Using tool: get_pds_contact
Response: Le contact professionnel de Adem Daami a été récupéré avec succès.
```

---

## 🧭 Roadmap

| Phase | Description                                  | Status     |
| ----- | -------------------------------------------- | ---------- |
| **1** | Project setup + config/logging               | ✅ Done     |
| **2** | Implement `get_pds_contact` tool             | ✅ Done     |
| **3** | Base agent using LangChain                   | ✅ Done     |
| **4** | Replace deprecated `.run()` with `.invoke()` | ✅ Done     |
| **5** | Add OAuth Manager                            | ✅ Done     |
| **6** | Transition to **LangGraph** agent            | 🔜 Next    |
| **7** | Add multiple tools + registry                | 🔜 Planned |
| **8** | Integration tests & FastAPI interface        | 🔜 Planned |
