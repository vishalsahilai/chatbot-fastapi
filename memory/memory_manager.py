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

def _get_redis():
    """Lazily initialize and return the Redis client."""
    global _redis_client
    if _redis_client is None:
        import redis
        _redis_client = redis.Redis(
            host=settings.redis_host, #Where Redis is running
            port=settings.redis_port, #Which port Redis is on
            db=settings.redis_db,     #Which Redis database
            password=settings.redis_password or None, #Password if set
            decode_responses=True,    #Return strings not bytes
        )
        logger.info(f"Redis connected: {settings.redis_host}:{settings.redis_port}")
    return _redis_client

# Internal: read / write session
def _read_session(session_id: str) -> dict:
    """Read session data from the configured backend."""
    if settings.memory_backend == "redis":
        raw = _get_redis().get(f"session:{session_id}")
        if raw:
            return json.loads(raw)
        return _empty_session()
    else:
        return _IN_MEMORY_STORE.get(session_id, _empty_session())

def _write_session(session_id: str, data: dict) -> None:
    """Write session data to the configured backend."""
    if settings.memory_backend == "redis":
        _get_redis().set(
            f"session:{session_id}",
            json.dumps(data),
            ex=86400,  # TTL: 24 hours
        )
    else:
        _IN_MEMORY_STORE[session_id] = data

def _empty_session() -> dict:
    """Returns the default empty session structure."""
    return {
        "summaries": [],
        "last_messages": [],
        "message_count": 0,
    }

# Public API
def get_session(session_id: str) -> dict:
    """
    Retrieves a session by ID.
    If session does not exist, returns a fresh empty session (auto-create).
    """
    session = _read_session(session_id)
    logger.debug(f"[{session_id}] Session loaded — msg_count={session['message_count']}")
    return session

def save_session(session_id: str, session: dict) -> None:
    """Persists the session back to the store."""
    _write_session(session_id, session)
    logger.debug(f"[{session_id}] Session saved — msg_count={session['message_count']}")

def increment_message_count(session: dict) -> dict:
    """Increments the message counter in the session object."""
    session["message_count"] += 1
    return session

def append_summary(session: dict, summary: dict) -> dict:
    """
    Appends a new summary to the session's summaries list.
    Enforces a rolling window of MAX_SUMMARIES (default: 5).
    Oldest summary is dropped when limit is exceeded.
    """
    session["summaries"].append(summary)
    if len(session["summaries"]) > settings.max_summaries:
        session["summaries"].pop(0)  # drop oldest
    return session

def set_last_messages(session: dict, user_msg: str, bot_response: str) -> dict:
    """
    Stores the most recent user message and bot response.
    This is used for phase-2 (full context) and for summarization input.
    """
    session["last_messages"] = [
        {"role": "user", "content": user_msg},
        {"role": "assistant", "content": bot_response},
    ]
    return session