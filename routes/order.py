from datetime import datetime, timezone
from database.models import orders_col
from services.customer_service import update_last_order
from services.sheets_service import save_order_to_sheets
from services.email_service import send_confirmation_email
from utils.logger import logger