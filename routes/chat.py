from fastapi import APIRouter
from pydantic import BaseModel
 
from services.chat_service import process_chat
from utils.validators import validate_message, validate_session_id
from utils.logger import logger
 
router = APIRouter()