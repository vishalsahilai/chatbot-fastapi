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

 
def test_save_and_retrieve_session():
    sid = "test_save_retrieve"
    session = _empty_session()
    session["message_count"] = 5
    save_session(sid, session)
 
    loaded = get_session(sid)
    assert loaded["message_count"] == 5
    delete_session(sid)
 