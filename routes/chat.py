from fastapi import APIRouter
from pydantic import BaseModel
 
from services.chat_service import process_chat
from utils.validators import validate_message, validate_session_id
from utils.logger import logger
 
router = APIRouter()

# Request Models
class ChatRequest(BaseModel):
    session_id: str
    message: str
 
    model_config = {
        "json_schema_extra": {
            "example": {
                "session_id": "user_abc123",
                "message": "What pizzas do you have?",
            }
        }
    }


# Response Models
class ChatResponse(BaseModel):
    session_id: str
    response: str
    message_count: int
 