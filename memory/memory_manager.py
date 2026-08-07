from datetime import datetime, timezone, timedelta
from database.models import sessions_col
from config.settings import settings
from utils.logger import logger


def _now() -> datetime:
    return datetime.now(timezone.utc)


def _is_expired(session: dict) -> bool:
    last_active = session.get("last_active")
    if not last_active:
        return False
    if isinstance(last_active, str):
        last_active = datetime.fromisoformat(last_active)
    # Fix timezone naive issue
    if last_active.tzinfo is None:
        last_active = last_active.replace(tzinfo=timezone.utc)
    return _now() - last_active > timedelta(hours=settings.session_timeout_hours)


def _empty_session(session_id: str, phone: str = "", name: str = "") -> dict:
    return {
        "session_id": session_id,
        "phone": phone,
        "name": name,
        "summaries": [],
        "last_messages": [],
        "message_count": 0,
        "created_at": _now().isoformat(),
        "last_active": _now().isoformat(),
        "is_expired": False,
        "order_state": {
            "collecting": False,
            "name": "",
            "phone": "",
            "email": "",
            "address": "",
            "items": [],
            "total": 0,
        },
    }


def get_session(session_id: str, phone: str = "", name: str = "") -> dict:
    doc = sessions_col().find_one({"session_id": session_id}, {"_id": 0})

    if not doc:
        session = _empty_session(session_id, phone, name)
        sessions_col().insert_one(session.copy())  # use copy
        logger.debug(f"[{session_id}] New session created.")
        return session

    if _is_expired(doc):
        logger.info(f"[{session_id}] Session expired — resetting.")
        session = _empty_session(session_id, doc.get("phone", phone), doc.get("name", name))
        sessions_col().replace_one({"session_id": session_id}, session.copy())  # ✅ use copy
        return session

    if "order_state" not in doc:
        doc["order_state"] = _empty_session(session_id)["order_state"]

    return doc


def save_session(session_id: str, session: dict):
    session["last_active"] = _now().isoformat()
    sessions_col().replace_one(
        {"session_id": session_id},
        session.copy(),  # use copy
        upsert=True
    )
    logger.debug(f"[{session_id}] Session saved.")


def increment_message_count(session: dict) -> dict:
    session["message_count"] += 1
    return session


def append_summary(session: dict, summary: dict) -> dict:
    session["summaries"].append(summary)
    return session  #  No limit — unlimited summaries


def set_last_messages(session: dict, user_msg: str, bot_response: str) -> dict:
    session["last_messages"] = [
        {"role": "user", "content": user_msg},
        {"role": "assistant", "content": bot_response},
    ]
    return session


def update_order_state(session: dict, updates: dict) -> dict:
    session["order_state"].update(updates)
    return session


def reset_order_state(session: dict) -> dict:
    session["order_state"] = {
        "collecting": False,
        "name": "",
        "phone": "",
        "email": "",
        "address": "",
        "items": [],
        "total": 0,
    }
    return session


def delete_session(session_id: str):
    sessions_col().delete_one({"session_id": session_id})
    logger.info(f"[{session_id}] Session deleted.")