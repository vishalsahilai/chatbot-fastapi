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