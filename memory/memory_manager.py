"""
Sadabahar Restaurant Chatbot — Memory Manager
Manages per-session storage with support for:
  - In-memory dict  (MEMORY_BACKEND=dict)  ← default for demo
  - Redis           (MEMORY_BACKEND=redis) ← recommended for production
 
Session structure:
{
    "session_id": {
        "summaries": [          ← max 5 rolling summaries
            {
                "user_intent": "...",
                "bot_response": "...",
                "context": "..."
            }
        ],
        "last_messages": [      ← current message + last bot response
            {"role": "user",      "content": "..."},
            {"role": "assistant", "content": "..."}
        ],
        "message_count": int    ← total messages in this session
    }
}
"""

import json
from typing import Optional

from config.settings import settings
from utils.logger import logger

# In-Memory Store (demo / single-process)
_IN_MEMORY_STORE: dict ={}

# Redis Client (lazy init)
_redis_client = None