from datetime import datetime, timezone
from fastapi import APIRouter
from pydantic import BaseModel
 
from config.settings import settings
 
router = APIRouter()

class HealthResponse(BaseModel):
    status: str
    service: str
    version: str
    environment: str
    memory_backend: str
    timestamp: str