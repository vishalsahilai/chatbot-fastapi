from datetime import datetime, timezone
from fastapi import APIRouter
from pydantic import BaseModel
 
from config.settings import settings
 
router = APIRouter()
