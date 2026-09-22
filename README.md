# 🛍️ ShopEase: Agentic AI Customer Support System

![Python](https://img.shields.io/badge/Python-3.11%2B-3776AB?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-backend-009688?logo=fastapi&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-frontend-FF4B4B?logo=streamlit&logoColor=white)
![LangChain](https://img.shields.io/badge/LangChain-agent-1C3C3C?logo=langchain&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-database-4169E1?logo=postgresql&logoColor=white)
![Chroma](https://img.shields.io/badge/ChromaDB-vector%20store-6E56CF)


An **agentic AI customer support system** for an e-commerce store. Instead of a hard-coded intent router, the **LLM decides which tools to call** to track orders, check refund eligibility, search a knowledge base (RAG), or escalate to a human, all while keeping persistent conversation state in PostgreSQL.

> **TL;DR:** LLM-driven tool calling (LangChain + Groq) over a FastAPI backend and PostgreSQL, with RAG over a support-policy knowledge base (Chroma), confirmation guardrails before refunds, human escalation via support tickets, and LangSmith tracing + automated evaluation (4/5 passing). Frontend is a Streamlit e-commerce site with a floating chat widget.

---

## 📸 Screenshots

| Chat widget (welcome) | Answer from RAG + tool details |
|---|---|
| ![Welcome](images/chat-welcome.png) | ![Refund policy](images/chat-refund-policy.png) |


---

## ✨ Features

**Agent and tools**
- LLM-driven tool selection using LangChain `bind_tools` (no `if "where" in message` logic)
- Multi-step, multi-tool reasoning (e.g. order details → order status → refund eligibility in one answer)
- Tools: `get_order_status`, `get_order_details`, `get_shipping_tracking`, `check_refund_eligibility_tool`, `search_knowledge_tool`, `create_support_ticket_tool`

**Refund workflow with guardrails**
- Eligibility rules: order delivered, within 7 days of delivery, no previous refund
- **Explicit confirmation required** before any refund is processed
- Pending actions are stored in PostgreSQL, so the workflow continues across messages

**RAG (Retrieval-Augmented Generation)**
- Knowledge base chunked, embedded, and stored in a persistent Chroma vector store
- The agent chooses RAG only when the question needs general support knowledge
- Grounded answers: the agent does not invent details missing from the knowledge base

**Human escalation**
- Creates a support ticket (e.g. `TICKET-F34B53F3`) when the AI cannot safely resolve an issue
- The trusted `conversation_id` is injected by the application, never invented by the LLM

**Observability and evaluation**
- Custom lightweight agent logger (tools, arguments, duration, success/failure)
- LangSmith tracing for full agent execution
- LangSmith dataset and automated evaluation script comparing expected vs. actual tool usage

**Frontend**
- ShopEase-style shopping homepage (navbar, hero, categories, benefits, footer)
- Floating support button with an open/close chat window
- Per-message **Tools Used** and **Agent Log** expanders for debugging

---

## 🏗️ Architecture

```
Customer
   ↓
Streamlit (ShopEase UI + floating chat)
   ↓
FastAPI  (/chat)
   ↓
AI Agent (Groq LLM + LangChain tool calling)
   ↓
Tools → Services → PostgreSQL / Chroma Vector DB
   ↓
Tool results → LLM → Final response
```

Business logic lives in a **service layer**, so the agent's tools stay thin and the database logic stays independent of the AI layer.

---

## 🧰 Tech Stack

| Area | Technology |
|---|---|
| LLM | Groq |
| Agent / Tool Calling | LangChain |
| Backend | FastAPI |
| Frontend | Streamlit |
| Database | PostgreSQL |
| ORM | SQLAlchemy 2.x, psycopg2-binary |
| RAG | LangChain + Chroma |
| Embeddings | OpenRouter embedding API (1024 dimensions) |
| Observability | LangSmith |
| Language | Python |

---

## 🗄️ Database Schema

- `customers`: id, name, email
- `orders`: status, expected delivery, product, quantity, price, carrier, tracking number, current location, delivered date
- `refunds`: order, amount, status, created/processed time
- `conversations`: conversation id, pending action, pending data, timestamps
- `support_tickets`: ticket id, conversation, order, issue, status, priority, timestamps

---

## 📁 Project Structure

```
CustomerSupport/
├── backend/
│   ├── main.py            # FastAPI app entry point
│   ├── routers/           # API routes (/chat)
│   ├── tools/             # LLM-facing tools
│   ├── services/          # Order, refund, conversation, ticket, knowledge services
│   ├── models/            # SQLAlchemy models
│   ├── config/            # App and database configuration
│   ├── data/              # Knowledge base documents and seed data
│   ├── scripts/           # Setup scripts (DB seeding, indexing)
│   ├── tests/             # Evaluation scripts (LangSmith)
│   └── chroma_db/         # Persistent vector store (git-ignored)
├── frontend/
│   ├── app.py             # Streamlit ShopEase UI + floating chat widget
│   └── tests/
├── images/                # README screenshots
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

---

## 🚀 Getting Started

### 1. Clone the repository
```bash
git clone https://github.com/YOUR-USERNAME/YOUR-REPO.git
cd YOUR-REPO
```

### 2. Create a virtual environment and install dependencies
```bash
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Set up PostgreSQL
Create a database (e.g. `shopease`) and note the connection string.

### 4. Configure environment variables
Create a `.env` file (see `.env.example`):

```env
GROQ_API_KEY=your_groq_key
OPENROUTER_API_KEY=your_openrouter_key
DATABASE_URL=postgresql://user:password@localhost:5432/shopease

LANGSMITH_TRACING=true
LANGSMITH_API_KEY=your_langsmith_key
LANGSMITH_PROJECT=customer-support-agent
```

### 5. Start the backend
```bash
cd backend
uvicorn main:app --reload
```

### 6. Start the frontend (in a new terminal)
```bash
cd frontend
streamlit run app.py
```

Open the Streamlit URL, click the floating support button, and start chatting.

---

## 💬 Example Conversations

| User says | What the agent does |
|---|---|
| "Where is my order ORD-1008?" | Calls `get_order_status` / `get_shipping_tracking` |
| "What is your refund policy?" | Calls `search_knowledge_tool` (RAG) |
| "Can I get a refund for ORD-1008?" | Calls `check_refund_eligibility_tool` |
| "Tell me the product, price, status, and refund eligibility of ORD-1008" | Chains multiple tools in one response |
| "I want to talk to a human" | Calls `create_support_ticket_tool` and returns a ticket ID |

---

## 🧪 Evaluation

A LangSmith dataset (`customer-support-agent-v1`) covers refund eligibility, human escalation, RAG policy retrieval, multi-tool queries, and order status.

```bash
cd backend
python tests/evaluate_agent.py
```

The script runs each question against the FastAPI backend, extracts the tools actually used, and compares them to the expected tools.

**Latest result: 4/5 passed.** The one miss was a case where two tools (`get_order_status` and `get_shipping_tracking`) could both validly answer the question, which exposed a limitation in the evaluator rather than the agent. The next step is supporting `required_tools` and `required_any_tools` in the evaluator.

---

## 🐛 Notable Problems Solved

- **Foreign-key failure on ticket creation:** a new conversation did not yet exist in `conversations`, so `support_tickets.conversation_id` violated the FK. Fixed by calling `ensure_conversation()` before processing each request.
- **Embedding dimension mismatch in Chroma:** resolved by resetting the old collection and re-indexing with 1024-dimension vectors.
- **Floating chat widget in Streamlit:** `st.chat_input` is page-level, so it was replaced with a form-based input inside a fixed-position container.

---

## 🛣️ Roadmap

- Improve evaluation semantics and expand guardrail tests
- Record and compare experiments in LangSmith
- Database migrations (Alembic)
- Authentication
- Deployment and production hardening


---

## 👤 Author

**Lajina Devale**

[GitHub](https://github.com/LajinaD) · [LinkedIn](https://www.linkedin.com/in/lajinadevale/)
