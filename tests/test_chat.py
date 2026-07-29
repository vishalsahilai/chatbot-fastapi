import pytest
from unittest.mock import AsyncMock, patch
from fastapi.testclient import TestClient
 
from main import app
 
client = TestClient(app)

# Health Endpoint
def test_health_returns_200():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["service"] == "Sadabahar Restaurant Chatbot"
    assert "timestamp" in data

# Chat Endpoint — Input Validation
def test_chat_empty_message_returns_400():
    response = client.post("/chat", json={"session_id": "test1", "message": ""})
    assert response.status_code == 400
    assert "empty" in response.json()["detail"].lower()

def test_chat_whitespace_message_returns_400():
    response = client.post("/chat", json={"session_id": "test1", "message": "   "})
    assert response.status_code == 400

def test_chat_empty_session_id_returns_400():
    response = client.post("/chat", json={"session_id": "", "message": "Hello"})
    assert response.status_code == 400

def test_chat_message_too_long_returns_400():
    long_msg = "a" * 2001
    response = client.post("/chat", json={"session_id": "test1", "message": long_msg})
    assert response.status_code == 400
    assert "too long" in response.json()["detail"].lower() 

def test_chat_missing_fields_returns_422():
    response = client.post("/chat", json={"message": "Hello"})
    assert response.status_code == 422