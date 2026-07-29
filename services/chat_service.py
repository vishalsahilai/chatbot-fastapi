from fastapi import HTTPException
 
from memory.memory_manager import (
    get_session,
    save_session,
    increment_message_count,
    append_summary,
    set_last_messages,
)
from memory.context_builder import get_context_for_llm
from memory.summarizer import summarize_conversation
from services.llm_service import safe_invoke_llm, get_summarizer_llm
from utils.logger import logger 

async def process_chat(session_id: str, user_message: str) -> dict:
    """
    Main chat handler. Called by the /chat route.
 
    Args:
        session_id   : Unique identifier for this user's session.
        user_message : The validated user message string.
 
    Returns:
        {
            "session_id"    : str,
            "response"      : str,
            "message_count" : int
        }
 
    Raises:
        HTTPException 503 if LLM is unavailable.
    """

    # Load session  
    session = get_session(session_id)
    msg_count = session["message_count"]
    logger.info(f"[{session_id}] Processing message #{msg_count + 1}: '{user_message[:60]}...'")

    # Build context
    context = get_context_for_llm(session, user_message)
    logger.debug(f"[{session_id}] Context built ({len(context)} chars)")

    # Invoke LLM
    try:
        bot_response = await safe_invoke_llm(context)
    except Exception as e:
        logger.error(f"[{session_id}] LLM failure: {e}")
        raise HTTPException(
            status_code=503,
            detail="LLM service is temporarily unavailable. Please try again in a moment.",
        )

    # Update memory
    session = increment_message_count(session)
 
    # For message 3+, generate and store a summary of the PREVIOUS exchange.
    # (We summarize the just-completed turn and store it.)
    if session["message_count"] >= 2:
        try:
            summary = await summarize_conversation(
                user_message=user_message,
                bot_response=bot_response,
                llm_chain=get_summarizer_llm(),
            )
            session = append_summary(session, summary)
            logger.debug(f"[{session_id}] Summary appended. Total summaries: {len(session['summaries'])}")
        except Exception as e:
            # Non-fatal: log and continue without summary
            logger.warning(f"[{session_id}] Summarization skipped: {e}")
 
    # Always update last_messages for context
    session = set_last_messages(session, user_message, bot_response)

    # Persist session
    save_session(session_id, session)
 
    logger.info(f"[{session_id}] Response sent ({len(bot_response)} chars)")
 
    return {
        "session_id": session_id,
        "response": bot_response,
        "message_count": session["message_count"],
    }
 