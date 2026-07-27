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


    #Second message — send full previous exchange
    if msg_count == 1 and last_messages:
        logger.debug("Context phase: 2 (second message — full prior exchange)")
        prev_user = last_messages[0]["content"] if len(last_messages) > 0 else ""
        prev_bot = last_messages[1]["content"] if len(last_messages) > 1 else ""
 
        context = (
            "[Previous Conversation]\n"
            f"User: {prev_user}\n"
            f"Assistant: {prev_bot}\n\n"
            f"[Current Message]\n{current_message}"
        )
        return context

    #Third message and beyond — summaries only

    logger.debug(f"Context phase: 3+ (msg #{msg_count + 1} — using {len(summaries)} summaries)")
 
    if not summaries:
        # Safety fallback: no summaries yet, just send current message
        return current_message
    
    summary_lines = ["[Conversation Summary]"]
    for i, s in enumerate(summaries, 1):
        summary_lines.append(
            f"\n[Exchange {i}]\n"
            f"  User Intent  : {s.get('user_intent', '')}\n"
            f"  Bot Response : {s.get('bot_response', '')}\n"
            f"  Context      : {s.get('context', '')}"
        )
 
    summary_lines.append(f"\n[Current Message]\n{current_message}")
 
    return "\n".join(summary_lines)
 
 
