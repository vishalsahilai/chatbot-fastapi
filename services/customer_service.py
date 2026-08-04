from datetime import datetime, timezone
from database.models import customers_col
from utils.logger import logger

def get_customer(phone: str) -> dict | None:
    return customers_col().find_one({"phone": phone}, {'_id':0})