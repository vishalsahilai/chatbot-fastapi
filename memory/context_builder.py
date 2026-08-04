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

    if msg_count == 1 and last_messages:
        logger.debug("Context phase: 2")
        prev_user = last_messages[0]["content"] if len(last_messages) > 0 else ""
        prev_bot = last_messages[1]["content"] if len(last_messages) > 1 else ""
        return (
            f"{name_context}"
            f"[Previous Conversation]\n"
            f"User: {prev_user}\n"
            f"Assistant: {prev_bot}\n\n"
            f"[Current Message]\n{current_message}"
        )

    logger.debug(f"Context phase: 3+ ({len(summaries)} summaries)")

    if not summaries:
        return f"{name_context}{current_message}"

    summary_lines = ["[Conversation Summary]"]
    for i, s in enumerate(summaries, 1):
        summary_lines.append(
            f"\n[Exchange {i}]\n"
            f"  User Intent  : {s.get('user_intent', '')}\n"
            f"  Bot Response : {s.get('bot_response', '')}\n"
            f"  Context      : {s.get('context', '')}"
        )

    summary_lines.append(f"\n[Current Message]\n{current_message}")
    return f"{name_context}" + "\n".join(summary_lines)