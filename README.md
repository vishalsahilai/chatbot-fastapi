# 🍕 Sadabahar Restaurant Chatbot

> A production-ready AI-powered restaurant chatbot built with FastAPI, LangChain, Google Gemini, RAG, MongoDB, and Google Sheets — handling everything from menu queries to order placement and email confirmation.

---

## 🖥️ Live Preview

![Sadabahar Restaurant Chatbot UI](./docs/sadabahar-restaurant-demo.png)

> **Try it live:** [sadabahar-restaurant-bot.vercel.app](https://sadabahar-restaurant-bot.vercel.app)

---

## 📋 Table of Contents

1. [Overview](#overview)
2. [System Architecture](#system-architecture)
3. [Features](#features)
4. [How It Works](#how-it-works)
5. [File Structure](#file-structure)
6. [Prerequisites](#prerequisites)
7. [Setup & Installation](#setup--installation)
8. [Environment Variables](#environment-variables)
9. [API Reference](#api-reference)
10. [Memory System](#memory-system)
11. [RAG System](#rag-system)
12. [Customer Recognition](#customer-recognition)
13. [Order System](#order-system)
14. [Database Structure](#database-structure)
15. [Frontend](#frontend)
16. [Error Handling](#error-handling)
17. [Production Deployment](#production-deployment)
18. [Tech Stack](#tech-stack)
19. [Author](#author)

---

## Overview

**Sadabahar Restaurant Chatbot** is a full-stack conversational AI system that handles complete customer interactions — from greeting returning customers by name, answering menu questions with exact prices from a PDF database, taking orders step by step, saving them to Google Sheets, and sending HTML email confirmations.

The system is built around three core innovations:

- **Hybrid Summarization Memory** — keeps conversation context lean without losing history
- **RAG (Retrieval-Augmented Generation)** — retrieves exact prices and details from a restaurant PDF
- **Phone-based Customer Recognition** — remembers customers permanently, even after cache clears

---

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                   Black & Red Chat UI                       │
│              HTML + CSS + Vanilla JavaScript                │
└────────────────────────┬────────────────────────────────────┘
                         │ HTTP POST /chat
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                    FastAPI Backend                           │
│  /chat          /order          /health                     │
│                                                             │
│  ┌─────────────┐  ┌──────────────┐  ┌──────────────────┐   │
│  │ RAG Service │  │Memory Manager│  │   LLM Service    │   │
│  │  Pinecone   │  │  MongoDB     │  │ Gemini + Rotation│   │
│  │  HuggingFace│  │  Unlimited   │  │ 4 API Keys       │   │
│  │  all-MiniLM │  │  Summaries   │  │ Auto-rotate      │   │
│  └─────────────┘  └──────────────┘  └──────────────────┘   │
│                                                             │
│  ┌─────────────┐  ┌──────────────┐  ┌──────────────────┐   │
│  │  Customer   │  │    Order     │  │     Email        │   │
│  │  Service    │  │   Service    │  │    Service       │   │
│  │  Phone ID   │  │  MongoDB +   │  │  Gmail SMTP      │   │
│  │  Permanent  │  │  Sheets      │  │  HTML Template   │   │
│  └─────────────┘  └──────────────┘  └──────────────────┘   │
└─────────────────────────────────────────────────────────────┘
          │                │                    │
          ▼                ▼                    ▼
     MongoDB Atlas    Google Sheets        Gmail SMTP
     3 Collections     Order Logs          HTML Email
     (free 512MB)      (free)              (free)
          │
          ▼
       Pinecone
    Vector Database
      (free tier)
```

---

## Features

- **Hybrid 3-Phase Summarization Memory** — smart memory that keeps context without token bloat
- **Unlimited Session Summaries** — no cap on conversation history per session
- **2-Hour Session Expiry** — auto-resets after inactivity, name + order history kept forever
- **RAG System** — Pinecone vector database + HuggingFace embeddings retrieves exact prices from PDF
- **Anti-Hallucination** — bot only uses verified data from RAG + fallback price list
- **Phone-Based Customer Recognition** — permanent memory survives cache clear and device change
- **Last Order Reorder** — returning customers offered one-click reorder of previous order
- **Step-by-Step Order Collection** — collects item, size, quantity, name, phone, email, address one at a time
- **Automatic Order Processing** — detects order confirmation from chat, triggers full pipeline automatically
- **Google Sheets Integration** — every order logged as a new row automatically
- **HTML Email Confirmation** — branded confirmation email sent on every order
- **Gemini API Key Rotation** — supports up to 4 API keys, rotates automatically on quota hit
- **Menu Shortcut** — complete menu sent instantly without hitting RAG (saves tokens)
- **RAG Skip Logic** — skips vector search for phone numbers, emails, addresses (saves 10-15s)
- **Session Isolation** — each user's data completely separate, no cross-user leakage
- **Black & Red Themed UI** — professional restaurant-grade frontend

---

## How It Works

### Conversation Flow
```
User: "hi"
Bot: Loads session from MongoDB
     Checks if phone known → greets by name
     New user → warm welcome

User: "show me the menu"
Bot: Detects menu keyword → skips RAG
     Returns full formatted menu instantly (zero vector search cost)

User: "i want to order Margherita Pizza Large"
Bot: Starts order collection flow
     Step 1: Confirms item + size ✅ (already provided)
     Step 2: Asks quantity
     Step 3: Asks if anything else
     Step 4: Asks name
     Step 5: Asks phone
     Step 6: Asks email
     Step 7: Asks address
     Step 8: Shows complete summary with prices from RAG
     Step 9: Asks for confirmation

User: "yes confirm"
Bot: Detects JSON order block in LLM response
     → Saves order to MongoDB
     → Updates customer's last_order
     → Adds row to Google Sheets
     → Sends HTML email to customer
     → Returns order ID + estimated time
```

### RAG Flow
```
Sadabahar_Restaurant.pdf
         ↓
PyPDF loads → RecursiveCharacterTextSplitter (500 chars, 100 overlap)
         ↓
HuggingFace all-MiniLM-L6-v2 → 384-dimensional vectors
         ↓
Stored permanently in Pinecone (cloud, survives restarts)

User query → same embedding model → cosine similarity search
         ↓
Top 6 most relevant chunks retrieved
         ↓
Injected into LLM context before user message
         ↓
LLM answers with exact prices, policies, FAQs from PDF
```

### Memory Algorithm (3-Phase Hybrid)
```
Message 1   → Raw message sent directly to LLM
              No prior context needed

Message 2   → Full previous exchange included
              [user_msg_1 + bot_response_1 + current_msg]

Message 3+  → Summarization kicks in
              Each previous exchange → structured summary:
              {user_intent, bot_response, context}
              All summaries sent + current message
              No full history = no token bloat
              Unlimited summaries per session
```

---

## File Structure

```
sadabahar-restaurant-chatbot/
│
├── main.py                          ← FastAPI entry point
├── requirements.txt
├── render.yaml                      ← Render deployment config
├── .env.example
├── .gitignore
│
├── config/
│   ├── __init__.py
│   └── settings.py                  ← Pydantic BaseSettings + .env loader
│
├── database/
│   ├── __init__.py
│   ├── mongodb.py                   ← MongoDB connection (lazy init, singleton)
│   └── models.py                    ← Collection helpers (customers, sessions, orders)
│
├── routes/
│   ├── __init__.py
│   ├── chat.py                      ← POST /chat
│   ├── health.py                    ← GET /health
│   └── order.py                     ← POST /order
│
├── services/
│   ├── __init__.py
│   ├── chat_service.py              ← Full chat pipeline orchestration
│   ├── llm_service.py               ← Gemini LLM + 4-key rotation
│   ├── customer_service.py          ← Phone-based customer CRUD
│   ├── order_service.py             ← Order processing + pipeline trigger
│   ├── sheets_service.py            ← Google Sheets API integration
│   └── email_service.py             ← Gmail SMTP HTML email
│
├── memory/
│   ├── __init__.py
│   ├── memory_manager.py            ← MongoDB session store + 2hr expiry
│   ├── summarizer.py                ← LLM-based conversation summarizer
│   └── context_builder.py          ← 3-phase context assembly
│
├── rag/
│   ├── __init__.py
│   ├── rag_service.py               ← RAG orchestration + skip logic
│   ├── vector_store.py              ← Pinecone setup + similarity search
│   ├── document_loader.py           ← PyPDF loader + text splitter
│   └── embeddings.py                ← HuggingFace all-MiniLM-L6-v2
│
├── prompts/
│   └── system_prompt.py             ← Dynamic system prompt with customer context
│
├── utils/
│   ├── __init__.py
│   ├── validators.py                ← Input validation
│   ├── logger.py                    ← Loguru structured logging
│   └── menu.py                      ← Full menu + is_menu_request() + skip RAG keywords
│
├── data/
│   └── Sadabahar_Restaurant.pdf     ← Restaurant PDF (ingested into Pinecone)
│
├── scripts/
│   └── ingest.py                    ← One-time PDF → Pinecone ingestion script
│
├── frontend/
│   ├── index.html                   ← Chat UI
│   ├── style.css                    ← Black & Red theme
│   └── app.js                       ← Fetch API + session management
│
└── tests/
    ├── __init__.py
    ├── test_chat.py
    ├── test_memory.py
    └── test_rag.py
```

---

## Prerequisites

| Tool | Version / Notes |
|---|---|
| Python | **≥ 3.10 and < 3.12** |
| pip | Latest |
| Git | Latest |
| Google Gemini API Key | Free — [aistudio.google.com](https://aistudio.google.com) |
| Pinecone Account | Free — [pinecone.io](https://pinecone.io) |
| MongoDB Atlas | Free 512MB — [mongodb.com/atlas](https://mongodb.com/atlas) |
| Google Cloud Project | Free — Sheets API enabled |
| Gmail Account | App Password required |

> ⚠️ **Python must be ≥ 3.10 and < 3.12.** Python 3.12+ causes dependency conflicts with some LangChain packages.

---

## Setup & Installation

```bash
# Clone
git clone https://github.com/vishalsahilai/sadabahar-restaurant-chatbot.git
cd sadabahar-restaurant-chatbot

# Virtual environment
python -m venv venv
source venv/bin/activate        # macOS/Linux
venv\Scripts\activate           # Windows

# Install dependencies
pip install -r requirements.txt

# Environment variables
cp .env.example .env
# Open .env and fill in all values

# Ingest PDF into Pinecone (run once only)
python scripts/ingest.py

# Start backend
python -m uvicorn main:app --reload
```

Frontend:
```bash
cd frontend
python -m http.server 3000
# Visit http://localhost:3000
```

---

## Environment Variables

```env
# ── Gemini (up to 4 keys — auto-rotates on quota) ──
GOOGLE_API_KEY_1=
GOOGLE_API_KEY_2=
GOOGLE_API_KEY_3=
GOOGLE_API_KEY_4=
GEMINI_MODEL=gemini-2.5-flash-preview-05-20
LLM_TEMPERATURE=0.7
LLM_MAX_TOKENS=512

# ── MongoDB Atlas ──
MONGODB_URI=mongodb+srv://user:pass@cluster.mongodb.net/sadabahar

# ── Pinecone ──
PINECONE_API_KEY=
PINECONE_INDEX_NAME=sadabahar-restaurant

# ── Google Sheets ──
GOOGLE_SHEETS_ID=
GOOGLE_SERVICE_ACCOUNT_JSON={"type":"service_account",...}

# ── Email (Gmail App Password) ──
EMAIL_USERNAME=your-gmail@gmail.com
EMAIL_PASSWORD=your-16-digit-app-password
EMAIL_FROM=your-gmail@gmail.com

# ── App ──
APP_ENV=development
APP_HOST=0.0.0.0
APP_PORT=8000
DEBUG=true

# ── Session ──
SESSION_TIMEOUT_HOURS=2

# ── CORS ──
CORS_ORIGINS=["http://localhost:3000","http://127.0.0.1:3000"]
```

---

## API Reference

### `POST /chat`

```json
// Request
{
  "session_id": "user_abc123",
  "message": "What pizzas do you have?",
  "phone": "0300-1234567"
}

// Response
{
  "session_id": "user_abc123",
  "response": "We have 8 amazing pizzas! 🍕 Margherita starts at PKR 750...",
  "message_count": 1
}
```

### `POST /order`

```json
// Request
{
  "session_id": "user_abc123",
  "phone": "0300-1234567",
  "name": "Vishal",
  "email": "vishal@email.com",
  "address": "House 12, Street 5, Karachi",
  "items": [
    { "name": "Margherita Pizza", "size": "Large", "qty": 1, "price": 1750 }
  ],
  "total": 1750
}

// Response
{
  "order_id": "ORD-20260807-001",
  "status": "confirmed",
  "message": "Order placed! Confirmation sent to vishal@email.com",
  "estimated_time": "30-45 minutes"
}
```

### `GET /health`

```json
{
  "status": "healthy",
  "service": "Sadabahar Restaurant Chatbot",
  "version": "2.0.0",
  "environment": "production",
  "timestamp": "2026-08-07T02:00:00Z"
}
```

---

## Memory System

The chatbot uses a **3-phase hybrid summarization algorithm** to maintain conversation context without sending full history to the LLM on every message.

```
Phase 1 — Message 1:
  Input: current message
  No prior context. Clean start.

Phase 2 — Message 2:
  Input: [previous user msg] + [previous bot response] + [current message]
  Full exchange included once.

Phase 3 — Message 3 and beyond:
  Each completed exchange is summarized by the LLM into:
  {
    "user_intent": "what the user wanted",
    "bot_response": "what the bot said",
    "context": "important details to remember"
  }
  All summaries + current message sent to LLM.
  Full history never sent again. Unlimited summaries per session.

Session expiry (2 hours of inactivity):
  → All summaries deleted
  → Message count reset
  → Customer name + phone + last order kept forever in MongoDB
```

---

## RAG System

RAG (Retrieval-Augmented Generation) gives the chatbot access to the complete restaurant PDF — including exact prices, delivery charges, special offers, FAQs, and policies.

**Ingestion (run once):**
```
Sadabahar_Restaurant.pdf
  → PyPDFLoader reads all pages
  → RecursiveCharacterTextSplitter: 500 chars, 100 overlap
  → HuggingFace all-MiniLM-L6-v2 converts each chunk to 384-dim vector
  → Vectors stored permanently in Pinecone (cosine similarity, cloud)
```

**Query (every relevant message):**
```
User message → same embedding model → 384-dim vector
  → Pinecone cosine similarity search → top 6 chunks
  → Injected into LLM context before user message
  → LLM answers with exact data from PDF
```

**Smart Skip Logic:**
Messages like phone numbers, emails, addresses, and short confirmations ("yes", "no", "ok") skip RAG entirely — saving 10-15 seconds per message during order collection.

**Pinecone Index Settings:**
- Dimensions: `384`
- Metric: `cosine`
- Cloud: AWS us-east-1

---

## Customer Recognition

The system uses **phone number as a permanent customer identifier** — this survives browser cache clears and device changes, unlike session-based approaches.

```
New customer:
  Bot greets warmly
  Collects phone → name → saves to MongoDB customers collection
  All future visits recognized by phone

Returning customer (same browser):
  session_id in localStorage → MongoDB lookup → name loaded
  Greeted by name on first message
  If last order exists → offered to reorder

Returning customer (new browser / cache cleared):
  Bot asks for phone number
  MongoDB lookup → name + last order found instantly
  Greeted by name, last order shown, reorder offered
```

---

## Order System

Orders are triggered automatically when the LLM detects a confirmation. No manual API call needed from the frontend.

```
Customer confirms order in chat
         ↓
LLM returns structured JSON alongside message:
{"order_ready": true, "name": "...", "items": [...], "total": ...}
         ↓
chat_service.py detects JSON block
         ↓
process_order() called automatically:
  1. Generate unique Order ID (ORD-YYYYMMDD-NNN)
  2. Save full order to MongoDB orders collection
  3. Update customer's last_order in MongoDB customers collection
  4. Append row to Google Sheets
  5. Send HTML confirmation email via Gmail SMTP
         ↓
Bot responds: "✅ Order confirmed! ID: ORD-20260807-001
              Email sent. Estimated delivery: 30-45 minutes 🍕"
```

---

## Database Structure

### `customers` collection
```json
{
  "phone": "0300-1234567",
  "name": "Vishal",
  "first_seen": "2026-08-07T02:00:00Z",
  "last_seen": "2026-08-07T02:30:00Z",
  "last_order": {
    "order_id": "ORD-20260807-001",
    "items": [{"name": "Margherita Pizza", "size": "Large", "qty": 1, "price": 1750}],
    "total": 1750,
    "date": "2026-08-07"
  }
}
```

### `sessions` collection
```json
{
  "session_id": "user_abc123",
  "phone": "0300-1234567",
  "name": "Vishal",
  "summaries": [],
  "last_messages": [],
  "message_count": 0,
  "order_state": {},
  "created_at": "2026-08-07T02:00:00Z",
  "last_active": "2026-08-07T02:30:00Z",
  "is_expired": false
}
```

### `orders` collection
```json
{
  "order_id": "ORD-20260807-001",
  "phone": "0300-1234567",
  "name": "Vishal",
  "email": "vishal@email.com",
  "address": "House 12, Street 5, Karachi",
  "items": [{"name": "Margherita Pizza", "size": "Large", "qty": 1, "price": 1750}],
  "total": 1750,
  "status": "confirmed",
  "created_at": "2026-08-07T02:16:00Z"
}
```

---

## Frontend

Single-page chat UI built with vanilla HTML, CSS, and JavaScript.

| Property | Value |
|---|---|
| Background | `#0A0A0A` |
| Primary Color | `#CC0000` (Red) |
| Font | Inter + Playfair Display |
| Session ID | Auto-generated, stored in localStorage |
| Typing Indicator | Animated red dots |
| Timestamps | On every message |
| Mobile | Fully responsive |
| Quick Suggestions | View Pizzas, View Burgers, Delivery Info, Hours |

---

## Error Handling

| Scenario | Status | Behaviour |
|---|---|---|
| Empty message | `400` | Returns validation error |
| Message > 2000 chars | `400` | Returns too long error |
| LLM failure | `503` | Returns service unavailable |
| All 4 API keys exhausted | `503` | Returns service unavailable |
| RAG retrieval failure | `200` | Falls back to system prompt + hardcoded prices |
| MongoDB failure | `503` | Returns database unavailable |
| Order validation failed | `400` | Returns specific field error |
| Google Sheets failure | `200` | Logged as warning, order still confirmed |
| Email failure | `200` | Logged as warning, order still confirmed |
| Session expired | `200` | New session created, name + order kept |

---

## Production Deployment

### Backend → Render (Free)

```yaml
services:
  - type: web
    name: sadabahar-chatbot
    env: python
    plan: free
    buildCommand: pip install -r requirements.txt
    startCommand: python -m uvicorn main:app --host 0.0.0.0 --port $PORT
    envVars:
      - key: GOOGLE_API_KEY_1
        sync: false
      - key: GOOGLE_API_KEY_2
        sync: false
      - key: GOOGLE_API_KEY_3
        sync: false
      - key: GOOGLE_API_KEY_4
        sync: false
      - key: GEMINI_MODEL
        value: gemini-2.5-flash-preview-05-20
      - key: MEMORY_BACKEND
        value: dict
      - key: APP_ENV
        value: production
      - key: DEBUG
        value: false
```

### Frontend → Netlify (Free)

1. Go to netlify.com
2. Drag and drop the `frontend/` folder
3. Live in 30 seconds ✅

---

## Tech Stack

| Layer | Technology | Purpose |
|---|---|---|
| Backend | FastAPI (Python 3.10–3.11) | REST API framework |
| LLM Framework | LangChain | LLM orchestration |
| LLM Provider | Google Gemini | AI responses |
| Embeddings | HuggingFace all-MiniLM-L6-v2 | 384-dim text vectors |
| Vector Database | Pinecone | Similarity search (RAG) |
| PDF Processing | PyPDF + RecursiveCharacterTextSplitter | Document ingestion |
| Database | MongoDB Atlas | Sessions, customers, orders |
| Order Storage | Google Sheets API | Visual order dashboard |
| Email | Gmail SMTP | HTML order confirmations |
| Logging | Loguru | Structured logs |
| Retry Logic | Tenacity | LLM exponential backoff |
| Frontend | Vanilla HTML + CSS + JavaScript | Chat UI |
| Deployment | Render + Netlify | Free hosting |

---

## Author

**Vishal Sahil** — AI Automation Engineer

- 🌐 [vishalsahilai.vercel.app](https://vishalsahilai.vercel.app)
- 💼 [linkedin.com/in/vishal-sahil-ai](https://linkedin.com/in/vishal-sahil-ai)
- 🐙 [github.com/vishalsahilai](https://github.com/vishalsahilai)
- 📧 vishalsahilofficial@gmail.com

---

MIT License — Free to use, modify, and distribute.

> Built with ❤️ by Vishal Sahil · Powered by LangChain + Google Gemini