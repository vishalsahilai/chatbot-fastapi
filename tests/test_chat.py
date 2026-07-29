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
