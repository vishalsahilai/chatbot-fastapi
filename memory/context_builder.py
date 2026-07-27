from utils.logger import logger


def get_context_for_llm(session: dict, current_message: str) -> str:
    """
    Builds the complete input string to send to the LLM,
    based on the current message count (phase logic).
 
    Args:
        session         : The current session dict from memory_manager.
        current_message : The user's current (new) message.
 
    Returns:
        A formatted string to be passed as the human message to the LLM.
    """
    msg_count = session.get("message_count", 0)
    summaries = session.get("summaries", [])
    last_messages = session.get("last_messages", [])

    #First message — no prior context
    if msg_count == 0:
        logger.debug("Context phase: 1 (first message — no prior context)")
        return current_message

    