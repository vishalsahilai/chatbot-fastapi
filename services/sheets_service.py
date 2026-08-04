import json
import gspread
from google.oauth2.service_account import Credentials
from config.settings import settings
from utils.logger import logger

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

def _get_sheet():
    creds_json = json.loads(settings.google_service_account_json)
    creds = Credentials.from_service_account_info(creds_json, scopes=SCOPES)
    client = gspread.authorize(creds)
    return client.open_by_key(settings.google_sheets_id).sheet1


def save_order_to_sheets(order: dict):
    sheet = _get_sheet()
    items_text = ", ".join(
        f"{i['name']} ({i.get('size', '')}) x{i['qty']}"
        for i in order["items"]
    )
    row = [
        order["order_id"],
        order["created_at"],
        order["name"],
        order["phone"],
        order.get("email", ""),
        order["address"],
        items_text,
        f"PKR {order['total']}",
        order["status"],
    ]
    sheet.append_row(row)
    logger.info(f"Order {order['order_id']} saved to Google Sheets.")