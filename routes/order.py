from fastapi import APIRouter
from pydantic import BaseModel
from typing import List
from services.order_service import process_order