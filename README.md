# 🍕 Sadabahar Restaurant Chatbot System

> A production-ready AI-powered restaurant chatbot built with FastAPI, LangChain, and a hybrid summarization memory system.

---

## 🎨 Theme

| Property | Value |
|---|---|
| **Primary Color** | `#FF0000` (Red) |
| **Background Color** | `#0A0A0A` (Black) |
| **Accent Color** | `#CC0000` (Dark Red) |
| **Font** | Inter / Roboto |

---

## 📋 Table of Contents

1. [Overview](#overview)
2. [System Architecture](#system-architecture)
3. [Features](#features)
4. [File Structure](#file-structure)
5. [Setup & Installation](#setup--installation)
6. [Environment Variables](#environment-variables)
7. [API Reference](#api-reference)
8. [Memory System](#memory-system)
9. [Menu System](#menu-system)
10. [Frontend](#frontend)
11. [Development Phases](#development-phases)
12. [Error Handling](#error-handling)
13. [Testing](#testing)
14. [Production Deployment](#production-deployment)

---

## Overview

**Sadabahar Restaurant Chatbot** is a full-stack conversational AI system designed to handle customer interactions for a restaurant. It provides:

- Real-time menu recommendations
- Order guidance and delivery information
- Session-isolated conversations (no cross-user data leakage)
- Intelligent hybrid memory with progressive summarization
- A sleek Black & Red themed frontend

The system is built to be **production-ready**, **modular**, and **fully extensible**.

---

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        CLIENT (Browser)                     │
│                   Black & Red Chat UI (HTML/CSS/JS)         │
└────────────────────────┬────────────────────────────────────┘
                         │  HTTP POST /chat
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                    FastAPI Backend                           │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────┐  │
│  │   Routes     │  │  Middleware  │  │  Error Handlers  │  │
│  │  /chat       │  │  CORS        │  │  Validation      │  │
│  │  /health     │  │  Logging     │  │  LLM Fallback    │  │
│  └──────┬───────┘  └──────────────┘  └──────────────────┘  │
│         │                                                   │
│         ▼                                                   │
│  ┌──────────────────────────────────────────────────────┐   │
│  │               Chat Service                           │   │
│  │  ┌─────────────────┐   ┌──────────────────────────┐ │   │
│  │  │  Memory Manager │   │    LangChain LLM Chain   │ │   │
│  │  │  - summarize()  │   │    - System Prompt       │ │   │
│  │  │  - update()     │   │    - Context Builder     │ │   │
│  │  │  - get_context()│   │    - Response Generator  │ │   │
│  │  └────────┬────────┘   └──────────────────────────┘ │   │
│  └───────────┼────────────────────────────────────────--┘   │
└──────────────┼──────────────────────────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────────────────────────┐
│                   Memory Storage Layer                      │
│  In-Memory Dict (Demo) / Redis (Production)                 │
│                                                             │
│  {                                                          │
│    "session_id": {                                          │
│      "summaries": [...],   ← max 5 rolling summaries       │
│      "last_messages": [...] ← current + last bot response  │
│    }                                                        │
│  }                                                          │
└─────────────────────────────────────────────────────────────┘
```

---

## Features

### Core Features
- **Session Management** — Each user gets a unique `session_id`; conversations are fully isolated
- **Hybrid Summarization Memory** — Smart 3-phase memory that keeps context without bloating the LLM prompt
- **LangChain LLM Integration** — Powered by OpenAI GPT or any compatible LLM
- **Menu-Aware Responses** — Bot only recommends items from the defined JSON menu
- **Delivery Logic** — Enforces 10 km delivery radius and 9 AM–11 PM timing rules

### Technical Features
- REST API with FastAPI
- CORS-enabled for frontend integration
- Structured logging
- Graceful error handling (empty input, LLM failure, invalid sessions)
- Modular codebase (routes, services, memory, utils)

---

## File Structure

```
sadabahar-chatbot/
│
├── README.md                        ← This file
├── requirements.txt                 ← Python dependencies
├── .env                             ← Environment variables (never commit)
├── .env.example                     ← Example env file (safe to commit)
├── .gitignore
│
├── main.py                          ← FastAPI app entry point
│
├── routes/
│   ├── __init__.py
│   ├── chat.py                      ← POST /chat endpoint
│   └── health.py                    ← GET /health endpoint
│
├── services/
│   ├── __init__.py
│   ├── chat_service.py              ← Core chat orchestration logic
│   └── llm_service.py               ← LangChain LLM setup & invocation
│
├── memory/
│   ├── __init__.py
│   ├── memory_manager.py            ← Session memory store (dict/Redis)
│   ├── summarizer.py                ← summarize_conversation() logic
│   └── context_builder.py          ← get_context_for_llm() logic
│
├── utils/
│   ├── __init__.py
│   ├── validators.py                ← Input validation helpers
│   ├── logger.py                    ← Structured logging setup
│   └── menu.py                      ← Menu JSON definition
│
├── config/
│   ├── __init__.py
│   └── settings.py                  ← Pydantic settings / env loader
│
├── prompts/
│   └── system_prompt.py             ← Restaurant system prompt template
│
├── frontend/
│   ├── index.html                   ← Chat UI (Black & Red theme)
│   ├── style.css                    ← Custom styles
│   └── app.js                       ← Fetch API integration
│
└── tests/
    ├── __init__.py
    ├── test_chat.py                  ← Chat endpoint tests
    ├── test_memory.py                ← Memory logic unit tests
    └── test_llm.py                  ← LLM service tests
```

---

## Setup & Installation

### Prerequisites

| Tool | Version |
|---|---|
| Python | 3.10+ |
| pip | Latest |
| Git | Latest |
| OpenAI API Key | Required |
| Redis (optional) | 7.x for production |

### Step 1 — Clone the Repository

```bash
git clone https://github.com/your-org/sadabahar-chatbot.git
cd sadabahar-chatbot
```

### Step 2 — Create a Virtual Environment

```bash
python -m venv venv

# On macOS/Linux
source venv/bin/activate

# On Windows
venv\Scripts\activate
```

### Step 3 — Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4 — Set Up Environment Variables

```bash
cp .env.example .env
# Edit .env and add your OpenAI API key and other settings
```

### Step 5 — Run the Backend

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Step 6 — Open the Frontend

Open `frontend/index.html` in your browser, or serve it:

```bash
# Using Python's built-in server
cd frontend
python -m http.server 3000
```

Then visit: `http://localhost:3000`

---

## Environment Variables

Create a `.env` file in the project root:

```env
# ─────────────────────────────────────────
# LLM Configuration
# ─────────────────────────────────────────
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxx
OPENAI_MODEL=gpt-4o-mini
LLM_TEMPERATURE=0.7
LLM_MAX_TOKENS=512

# ─────────────────────────────────────────
# App Configuration
# ─────────────────────────────────────────
APP_ENV=development
APP_HOST=0.0.0.0
APP_PORT=8000
DEBUG=true

# ─────────────────────────────────────────
# Memory Configuration
# ─────────────────────────────────────────
MEMORY_BACKEND=dict          # Options: dict | redis
MAX_SUMMARIES=5

# ─────────────────────────────────────────
# Redis (only if MEMORY_BACKEND=redis)
# ─────────────────────────────────────────
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0
REDIS_PASSWORD=

# ─────────────────────────────────────────
# CORS
# ─────────────────────────────────────────
CORS_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
```

---

## API Reference

### `POST /chat`

Send a user message to the chatbot.

**Request Body:**

```json
{
  "session_id": "user_abc123",
  "message": "What pizzas do you have?"
}
```

**Success Response `200 OK`:**

```json
{
  "session_id": "user_abc123",
  "response": "We have two amazing pizzas — Margherita and Pepperoni! 🍕 The Margherita is a classic with fresh mozzarella and basil, while the Pepperoni is loaded with spicy pepperoni slices. Which one would you like to order?",
  "message_count": 1
}
```

**Error Response `400 Bad Request`:**

```json
{
  "detail": "Message cannot be empty."
}
```

**Error Response `503 Service Unavailable`:**

```json
{
  "detail": "LLM service is temporarily unavailable. Please try again."
}
```

---

### `GET /health`

Check if the service is running.

**Response `200 OK`:**

```json
{
  "status": "healthy",
  "service": "Sadabahar Restaurant Chatbot",
  "version": "1.0.0",
  "timestamp": "2025-07-25T10:30:00Z"
}
```

---

## Memory System

This is the core intelligence of the chatbot. It uses a **3-phase hybrid summarization** approach to keep LLM context lean and relevant.

### How It Works

```
Message 1
  └─→  Send directly to LLM (no prior context)

Message 2
  └─→  Send full conversation: [msg1 + bot_response1 + msg2]

Message 3+
  └─→  DO NOT send full history
       Instead:
         1. Summarize previous interaction(s)
         2. Store summary (keep last 5 max)
         3. Send to LLM:
            [All Summaries] + [Current User Message]
```

### Summary Structure

Each summary stored in memory follows this format:

```json
{
  "user_intent": "User asked about pizza options",
  "bot_response": "Recommended Margherita and Pepperoni pizzas",
  "context": "User appears interested in ordering pizza, exploring menu"
}
```

### Memory Store Structure

```python
SESSION_STORE = {
  "session_id_xyz": {
    "summaries": [
      {
        "user_intent": "...",
        "bot_response": "...",
        "context": "..."
      }
      # max 5 entries — oldest dropped when limit reached
    ],
    "last_messages": [
      {"role": "user", "content": "..."},
      {"role": "assistant", "content": "..."}
    ]
  }
}
```

### Core Memory Functions

| Function | Description |
|---|---|
| `summarize_conversation(user_msg, bot_response, context)` | Calls LLM to generate a structured summary of a single exchange |
| `update_memory(session_id, user_msg, bot_response)` | Updates the session's summaries list and last_messages; enforces max 5 summaries |
| `get_context_for_llm(session_id, current_message)` | Assembles the correct context block based on message count (phase 1, 2, or 3+) |

---

## Menu System

The menu is defined as a static JSON object in `utils/menu.py`. The LLM is **strictly instructed** to only recommend items from this list — no hallucination of menu items.

```json
{
  "pizza": [
    "Margherita",
    "Pepperoni"
  ],
  "burger": [
    "Zinger Burger",
    "Beef Burger"
  ],
  "drinks": [
    "Coca-Cola",
    "Mango Lassi",
    "Mineral Water"
  ],
  "sides": [
    "Garlic Bread",
    "Coleslaw",
    "French Fries"
  ],
  "desserts": [
    "Chocolate Brownie",
    "Gulab Jamun"
  ]
}
```

The full menu is injected into the system prompt at startup so the LLM always has access to it.

---

## Frontend

The frontend is a single-page chat interface served from the `frontend/` folder.

### Design Specs

| Element | Style |
|---|---|
| Background | `#0A0A0A` (near black) |
| Chat bubble (bot) | `#1A0000` with red border |
| Chat bubble (user) | `#CC0000` |
| Input bar | Dark gray with red focus ring |
| Send button | Red with hover glow |
| Font | `Inter`, sans-serif |
| Header | Restaurant name + logo, red accent |

### How It Connects

The frontend uses the native `fetch` API to call the backend:

```javascript
// Auto-generates a session_id stored in localStorage
const sessionId = localStorage.getItem('session_id') || generateUUID();

const response = await fetch('http://localhost:8000/chat', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    session_id: sessionId,
    message: userInput
  })
});
```

---

## Development Phases

### Phase 1 — Setup
- Initialize project structure
- Configure virtual environment
- Install base dependencies
- Set up `.env` and config loader

### Phase 2 — Backend
- Initialize FastAPI app in `main.py`
- Configure CORS and middleware
- Set up structured logging
- Register routes

### Phase 3 — LLM
- Set up LangChain with OpenAI
- Write system prompt in `prompts/system_prompt.py`
- Inject menu and restaurant rules into prompt
- Test basic LLM invocation

### Phase 4 — Memory
- Implement `memory_manager.py` with in-memory dict store
- Implement `summarizer.py` — calls LLM to generate summaries
- Implement `context_builder.py` — selects correct context based on message count
- Unit test all three memory functions

### Phase 5 — API
- Implement `POST /chat` route with full memory integration
- Implement `GET /health` route
- Add input validation and error handling
- Test all endpoints with Postman/cURL

### Phase 6 — Frontend
- Build chat UI in `frontend/index.html`
- Style with Black & Red theme in `style.css`
- Connect to backend via `fetch` in `app.js`
- Test end-to-end conversation flow

### Phase 7 — Testing
- Write unit tests for memory logic
- Write integration tests for chat endpoint
- Load test for concurrent sessions
- Verify no cross-session data leakage

---

## Error Handling

| Scenario | HTTP Status | Response |
|---|---|---|
| Empty message | `400` | `"Message cannot be empty."` |
| Message too long (>2000 chars) | `400` | `"Message too long."` |
| LLM timeout or failure | `503` | `"LLM service unavailable."` |
| Session not found (auto-created) | `200` | New session initialized transparently |
| Invalid JSON body | `422` | FastAPI default validation error |

---

## Testing

### Run All Tests

```bash
pytest tests/ -v
```

### Run Specific Test Files

```bash
pytest tests/test_memory.py -v
pytest tests/test_chat.py -v
```

### Manual API Test with cURL

```bash
# Health check
curl http://localhost:8000/health

# Send a chat message
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"session_id": "test123", "message": "What burgers do you have?"}'
```

---

## Production Deployment

### Switch to Redis Memory

In `.env`:

```env
MEMORY_BACKEND=redis
REDIS_HOST=your-redis-host
REDIS_PORT=6379
REDIS_PASSWORD=your-redis-password
```

### Run with Gunicorn

```bash
pip install gunicorn
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### Docker (Optional)

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

```bash
docker build -t sadabahar-chatbot .
docker run -p 8000:8000 --env-file .env sadabahar-chatbot
```

---

## Restaurant Info (Injected into System Prompt)

| Field | Value |
|---|---|
| **Name** | Sadabahar Restaurant |
| **Delivery Radius** | 10 km |
| **Operating Hours** | 9:00 AM – 11:00 PM |
| **Tone** | Friendly, helpful, enthusiastic |
| **Hallucination Policy** | Strictly prohibited — only menu items allowed |

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | FastAPI (Python 3.10+) |
| LLM Framework | LangChain |
| LLM Provider | OpenAI GPT-4o-mini (configurable) |
| Memory (demo) | In-memory Python dict |
| Memory (prod) | Redis |
| Frontend | Vanilla HTML / CSS / JavaScript |
| Testing | pytest |
| Server | Uvicorn / Gunicorn |

---

## License

MIT License — Free to use, modify, and distribute.

---

> Built with ❤️ for Sadabahar Restaurant. Powered by LangChain + FastAPI.