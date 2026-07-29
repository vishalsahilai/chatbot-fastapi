import pytest
from unittest.mock import AsyncMock, patch
from fastapi.testclient import TestClient
 
from main import app
 
client = TestClient(app)