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