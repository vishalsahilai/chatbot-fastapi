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

# Session Management Tests
def test_get_session_creates_empty_session():
    session = get_session("test_new_session_xyz")
    assert session["summaries"] == []
    assert session["last_messages"] == []
    assert session["message_count"] == 0