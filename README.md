# 🍕 Sadabahar Restaurant Chatbot

> Production-ready AI restaurant chatbot with hybrid memory, RAG, order placement, MongoDB persistence, and email confirmation.

---

## 🖥️ Live Preview

![Sadabahar Restaurant Chatbot UI](./docs/sadabahar-restaurant-demo.png)

> **Live:** [sadabahar-restaurant-bot.vercel.app](https://sadabahar-restaurant-bot.vercel.app)

---

## 📋 Table of Contents

1. [Overview](#overview)
2. [System Architecture](#system-architecture)
3. [Features](#features)
4. [File Structure](#file-structure)
5. [Prerequisites](#prerequisites)
6. [Setup & Installation](#setup--installation)
7. [Environment Variables](#environment-variables)
8. [API Reference](#api-reference)
9. [Memory System](#memory-system)
10. [RAG System](#rag-system)
11. [Customer Recognition](#customer-recognition)
12. [Order System](#order-system)
13. [Database Structure](#database-structure)
14. [Frontend](#frontend)
15. [Development Phases](#development-phases)
16. [Error Handling](#error-handling)
17. [Production Deployment](#production-deployment)
18. [Tech Stack](#tech-stack)
19. [Author](#author)

---

## Overview

**Sadabahar Restaurant Chatbot** is a full-stack conversational AI system that handles customer interactions end-to-end — from greeting returning customers by name, to taking orders, saving them to Google Sheets, and sending email confirmations.

---

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                   Black & Red Chat UI                       │
└────────────────────────┬────────────────────────────────────┘
                         │ HTTP POST /chat
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                    FastAPI Backend                           │
│  /chat   /order   /health                                   │
│                                                             │
│  ┌─────────────┐  ┌──────────────┐  ┌──────────────────┐   │
│  │ RAG Service │  │Memory Manager│  │   LLM Service    │   │
│  │  Pinecone   │  │  MongoDB     │  │ Gemini + Rotation│   │
│  └─────────────┘  └──────────────┘  └──────────────────┘   │
│                                                             │
│  ┌─────────────┐  ┌──────────────┐  ┌──────────────────┐   │
│  │  Customer   │  │    Order     │  │     Email        │   │
│  │  Service    │  │   Service    │  │    Service       │   │
│  └─────────────┘  └──────────────┘  └──────────────────┘   │
└─────────────────────────────────────────────────────────────┘
          │                │                    │
          ▼                ▼                    ▼
     MongoDB Atlas    Google Sheets        Gmail SMTP
     (free 512MB)      (free)               (free)
          │
     Pinecone
     (free tier)
```

---

## Features

### Part 1 — Core Chatbot
- Hybrid 3-phase summarization memory
- Unlimited session summaries
- Session isolation per user
- Gemini API key rotation (up to 4 keys)
- Anti-hallucination system prompt
- Black & Red themed frontend

### Part 2 — Advanced Features
- RAG system (Pinecone + HuggingFace + PDF)
- Customer recognition by phone number
- Permanent name memory (survives cache clear)
- Last order reorder suggestion on return visit
- Order placement through chat
- Google Sheets order logging
- Email confirmation on every order
- MongoDB for all persistent data
- 2-hour session inactivity expiry

---

## File Structure

```
sadabahar-restaurant-chatbot/
│
├── main.py
├── requirements.txt
├── render.yaml
├── .env.example
├── .gitignore
│
├── routes/
│   ├── chat.py
│   ├── health.py
│   └── order.py
│
├── services/
│   ├── chat_service.py
│   ├── llm_service.py
│   ├── customer_service.py
│   ├── order_service.py
│   ├── sheets_service.py
│   └── email_service.py
│
├── rag/
│   ├── rag_service.py
│   ├── vector_store.py
│   ├── document_loader.py
│   └── embeddings.py
│
├── memory/
│   ├── memory_manager.py
│   ├── summarizer.py
│   └── context_builder.py
│
├── database/
│   ├── mongodb.py
│   └── models.py
│
├── utils/
│   ├── validators.py
│   ├── logger.py
│   └── menu.py
│
├── config/
│   └── settings.py
│
├── prompts/
│   └── system_prompt.py
│
├── data/
│   └── Sadabahar_Restaurant.pdf
│
├── scripts/
│   └── ingest.py
│
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── app.js
│
└── tests/
    ├── test_chat.py
    ├── test_memory.py
    └── test_rag.py
```

---

## Prerequisites

| Tool | Version |
|---|---|
| Python | **≥ 3.10 and < 3.12** |
| pip | Latest |
| Git | Latest |
| Google Gemini API Key | Free — aistudio.google.com |
| Pinecone Account | Free — pinecone.io |
| MongoDB Atlas | Free — mongodb.com/atlas |
| Google Sheets API | Free |
| Gmail Account | Free |

> ⚠️ Python must be **≥ 3.10 and < 3.12**

---

## Setup & Installation

```bash
git clone https://github.com/vishalsahilai/sadabahar-restaurant-chatbot.git
cd sadabahar-restaurant-chatbot

python -m venv venv
source venv/bin/activate        # macOS/Linux
venv\Scripts\activate           # Windows

pip install -r requirements.txt

cp .env.example .env
# Fill in all values in .env

python scripts/ingest.py        # Run once to load PDF into Pinecone

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
# Gemini (up to 4 keys — auto-rotates on quota)
GOOGLE_API_KEY_1=
GOOGLE_API_KEY_2=
GOOGLE_API_KEY_3=
GOOGLE_API_KEY_4=
GEMINI_MODEL=gemini-2.5-flash-preview-05-20
LLM_TEMPERATURE=0.7
LLM_MAX_TOKENS=512

# MongoDB
MONGODB_URI=mongodb+srv://user:pass@cluster.mongodb.net/sadabahar

# Pinecone
PINECONE_API_KEY=
PINECONE_INDEX_NAME=sadabahar-restaurant

# Google Sheets
GOOGLE_SHEETS_ID=
GOOGLE_SERVICE_ACCOUNT_JSON=

# Email
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USERNAME=
EMAIL_PASSWORD=
EMAIL_FROM=

# App
APP_ENV=development
APP_HOST=0.0.0.0
APP_PORT=8000
DEBUG=true

# Memory
SESSION_TIMEOUT_HOURS=2

# CORS
CORS_ORIGINS=["http://localhost:3000","http://127.0.0.1:3000"]
```

---

## API Reference

### `POST /chat`
```json
// Request
{ "session_id": "user_abc", "message": "hi", "phone": "0300-1234567" }

// Response
{ "session_id": "user_abc", "response": "Welcome back Vishal! 😊", "message_count": 1 }
```

### `POST /order`
```json
// Request
{
  "session_id": "user_abc",
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
  "order_id": "ORD-20260801-001",
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
  "timestamp": "2026-08-01T05:16:00Z"
}
```

---

## Memory System

```
Message 1   → direct to LLM
Message 2   → full previous exchange + current message
Message 3+  → all summaries + current message (unlimited, no cap)

Session expires after 2 hours of inactivity:
  → summaries deleted
  → message count reset
  → name + phone + last order kept forever in MongoDB
```

---

## RAG System

```
PDF → chunks (500 chars) → HuggingFace vectors → Pinecone

User query → vector search → top 4 chunks → injected into LLM

Result: exact prices, delivery charges, FAQs from PDF
```

Run once:
```bash
python scripts/ingest.py
```

---

## Customer Recognition

```
New customer:
  Bot asks phone → asks name → saves to MongoDB

Returning customer (same browser):
  session_id in localStorage → name loaded → greeted by name
  If has last order → bot offers to reorder

Returning customer (cache cleared):
  Bot asks phone → MongoDB lookup → name found → greeted by name
  Last order shown → reorder option offered
```

---

## Order System

```
Customer places order through chat
         ↓
POST /order
         ↓
Order saved to MongoDB (orders collection)
Last order updated in MongoDB (customers collection)
Row added to Google Sheets
Confirmation email sent to customer
         ↓
Bot confirms with order ID + estimated time
```

### Email Template
```
Subject: Order Confirmed — Sadabahar Restaurant 🍕

Dear Vishal,

Your order ORD-20260801-001 has been confirmed!

Items:
- Margherita Pizza (Large) x1 — PKR 1,750

Total: PKR 1,750 + PKR 100 delivery = PKR 1,850
Estimated delivery: 30-45 minutes

📞 +92 336 6874263
```

---

## Database Structure

### customers
```json
{
  "phone": "0300-1234567",
  "name": "Vishal",
  "first_seen": "2026-08-01",
  "last_seen": "2026-08-01",
  "last_order": {
    "order_id": "ORD-20260801-001",
    "items": [{"name": "Margherita Pizza", "size": "Large", "qty": 1, "price": 1750}],
    "total": 1750,
    "date": "2026-08-01"
  }
}
```

### sessions
```json
{
  "session_id": "user_abc123",
  "phone": "0300-1234567",
  "name": "Vishal",
  "summaries": [],
  "last_messages": [],
  "message_count": 0,
  "created_at": "2026-08-01T05:00:00",
  "last_active": "2026-08-01T05:30:00",
  "is_expired": false
}
```

### orders
```json
{
  "order_id": "ORD-20260801-001",
  "phone": "0300-1234567",
  "name": "Vishal",
  "email": "vishal@email.com",
  "address": "House 12, Street 5",
  "items": [],
  "total": 1750,
  "status": "confirmed",
  "created_at": "2026-08-01T05:16:00"
}
```

---

## Frontend

| Element | Value |
|---|---|
| Background | `#0A0A0A` |
| Primary | `#CC0000` |
| Font | Inter + Playfair Display |
| Features | Session ID, typing indicator, timestamps, mobile responsive |

---

## Development Phases

**Part 1:**
- Phase 1 — Setup + venv
- Phase 2 — FastAPI + CORS
- Phase 3 — Gemini + system prompt
- Phase 4 — Hybrid memory system
- Phase 5 — API endpoints
- Phase 6 — Frontend UI
- Phase 7 — Testing + deployment

**Part 2:**
- Phase 8 — RAG (Pinecone + HuggingFace + PDF)
- Phase 9 — MongoDB integration
- Phase 10 — Customer recognition + name memory
- Phase 11 — Order placement system
- Phase 12 — Google Sheets integration
- Phase 13 — Email confirmation
- Phase 14 — End-to-end testing + production

---

## Error Handling

| Scenario | Status | Response |
|---|---|---|
| Empty message | `400` | Message cannot be empty |
| Message too long | `400` | Message too long |
| LLM failure | `503` | LLM service unavailable |
| All API keys exhausted | `503` | LLM service unavailable |
| RAG failure | `200` | Falls back to system prompt |
| MongoDB failure | `503` | Database unavailable |
| Order validation failed | `400` | Validation error |
| Email failed | `200` | Order saved, email logged |

---

## Production Deployment

```yaml
# render.yaml
services:
  - type: web
    name: sadabahar-chatbot
    env: python
    plan: free
    buildCommand: pip install -r requirements.txt
    startCommand: python -m uvicorn main:app --host 0.0.0.0 --port $PORT
```

Frontend → Netlify (drag and drop `frontend/` folder)

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | FastAPI (Python 3.10–3.11) |
| LLM | LangChain + Google Gemini |
| RAG Vector DB | Pinecone (free) |
| Embeddings | HuggingFace all-MiniLM-L6-v2 |
| Database | MongoDB Atlas (free) |
| Order Storage | Google Sheets (free) |
| Email | Gmail SMTP (free) |
| Frontend | HTML + CSS + JavaScript |
| Deployment | Render + Netlify (free) |

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