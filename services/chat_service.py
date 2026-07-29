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