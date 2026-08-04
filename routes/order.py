from datetime import datetime, timezone
from database.models import orders_col
from services.customer_service import update_last_order
from services.sheets_service import save_order_to_sheets
from services.email_service import send_confirmation_email
from utils.logger import logger

def generate_order_id() -> str:
    now = datetime.now(timezone.utc)
    count = orders_col().count_documents({})
    return f"ORD-{now.strftime('%Y%m%d')}-{str(count + 1).zfill(3)}"

async def process_order(order_data: dict) -> dict:
    order_id = generate_order_id()
    order = {
        "order_id": order_id,
        "phone": order_data["phone"],
        "name": order_data["name"],
        "email": order_data.get("email", ""),
        "address": order_data["address"],
        "items": order_data["items"],
        "total": order_data["total"],
        "status": "confirmed",
        "created_at": datetime.now(timezone.utc).isoformat(),
    }

    orders_col().insert_one({**order})
    logger.info(f"Order saved to MongoDB: {order_id}")
 
    last_order_summary = {
        "order_id": order_id,
        "items": order_data["items"],
        "total": order_data["total"],
        "date": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
    }
    update_last_order(order_data["phone"], last_order_summary)