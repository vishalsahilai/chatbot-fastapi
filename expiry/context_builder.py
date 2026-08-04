
from utils.logger import logger
 
 
def get_context_for_llm(session: dict, current_message: str) -> str:
    msg_count = session.get("message_count", 0)
    summaries = session.get("summaries", [])
    last_messages = session.get("last_messages", [])
    name = session.get("name", "")
 
    name_context = f"Customer name: {name}\n\n" if name else ""
 
    if msg_count == 0:
        logger.debug("Context phase: 1")
        return f"{name_context}{current_message}"