"""
Sadabahar Restaurant Chatbot — Chat Service (with RAG)"""

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
from rag.rag_service import get_rag_context
from utils.logger import logger


async def process_chat(session_id: str, user_message: str) -> dict:
    """
    Main chat handler with RAG integration.

    Pipeline:
        1. Load session
        2. Get RAG context from ChromaDB
        3. Build memory context (3-phase)
        4. Combine RAG + memory context
        5. Invoke LLM
        6. Update memory
        7. Return response
    """
    #  Step 1: Load session 
    session = get_session(session_id)
    msg_count = session["message_count"]
    logger.info(f"[{session_id}] Message #{msg_count + 1}: '{user_message[:60]}'")

    #  Step 2: Retrieve RAG context 
    rag_context = get_rag_context(user_message)
    if rag_context:
        logger.debug(f"[{session_id}] RAG context retrieved ({len(rag_context)} chars)")
    else:
        logger.debug(f"[{session_id}] No RAG context for this query")

    #  Step 3: Build memory context (3-phase) 
    memory_context = get_context_for_llm(session, user_message)

    #  Step 4: Combine RAG + memory context 
    if rag_context:
        full_context = f"{rag_context}\n\n{memory_context}"
    else:
        full_context = memory_context

    logger.debug(f"[{session_id}] Full context built ({len(full_context)} chars)")

    #  Step 5: Invoke LLM
    try:
        bot_response = await safe_invoke_llm(full_context)
    except Exception as e:
        logger.error(f"[{session_id}] LLM failure: {e}")
        raise HTTPException(
            status_code=503,
            detail="LLM service is temporarily unavailable. Please try again in a moment.",
        )

    #  Step 6: Update memory 
    session = increment_message_count(session)

    if session["message_count"] >= 2:
        try:
            summary = await summarize_conversation(
                user_message=user_message,
                bot_response=bot_response,
                llm_chain=get_summarizer_llm(),
            )
            session = append_summary(session, summary)
            logger.debug(f"[{session_id}] Summary appended. Total: {len(session['summaries'])}")
        except Exception as e:
            logger.warning(f"[{session_id}] Summarization skipped: {e}")

    session = set_last_messages(session, user_message, bot_response)

    #  Step 7: Persist session 
    save_session(session_id, session)
    logger.info(f"[{session_id}] Response sent ({len(bot_response)} chars)")

    return {
        "session_id": session_id,
        "response": bot_response,
        "message_count": session["message_count"],
    }