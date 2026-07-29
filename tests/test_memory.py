import pytest
from memory.memory_manager import (
    get_session,
    save_session,
    increment_message_count,
    append_summary,
    set_last_messages,
    delete_session,
    _empty_session,
)
from memory.context_builder import get_context_for_llm