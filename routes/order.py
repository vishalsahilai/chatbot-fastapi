from fastapi import APIRouter
from pydantic import BaseModel
from typing import List
from services.order_service import process_order

router = APIRouter()

class OrderItem(BaseModel):
    name: str
    size: str = ""
    qty: int
    price: float