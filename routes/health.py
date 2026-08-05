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

@router.get(
    "/health",
    response_model=HealthResponse,
    summary="Health check",
    tags=["System"],
)
async def health() -> HealthResponse:
    """
    Returns the current health status of the chatbot service.
    Use this endpoint for uptime monitoring and deployment checks.
    """
    return HealthResponse(
        status="healthy",
        service="Sadabahar Restaurant Chatbot",
        version="2.0.0",
        environment=settings.app_env,
        memory_backend="MongoDB",
        timestamp=datetime.now(timezone.utc).isoformat(),
    )