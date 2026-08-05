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

class OrderRequest(BaseModel):
    session_id: str
    phone: str
    name: str
    eamil: str = ""
    address: str
    items: list[OrderItem]
    total: float

class OrderResponse(BaseModel):
    order_id: str
    status: str
    message: str
    estimated_time: str

@router.post("/order", response_model=OrderResponse, tags=["Order"])
async def place_order(request: OrderResponse) -> OrderResponse:
    order_data = request.model_dump()
    order_data["items"] = [item.model_dump() for item in request.items]
    result = await process_order(order_data)
    return OrderResponse(**result)