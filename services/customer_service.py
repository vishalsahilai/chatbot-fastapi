from datetime import datetime, timezone
from database.models import customers_col
from utils.logger import logger

def get_customer(phone: str) -> dict | None:
    return customers_col().find_one({"phone": phone}, {'_id':0})

def create_customer(phone: str, name: str) -> dict:
    customer = {
        "phone": phone,
        "name": name,
        "first_seen": datetime.now(timezone.utc).isoformat(),
        "last_seen": datetime.now(timezone.utc).isoformat(),
        "last_order": None,
    }
    customers_col().insert_one({**customer})
    logger.info(f"New customer created: {name} ({phone})")
    return customer

def update_last_seen(phone: str):
    customers_col().update_one(
        {"phone": phone},
        {"$set": {"last_seen": datetime.now(timezone.utc).isoformat()}}
    )

def update_last_order(phone: str, order: dict):
    customers_col().update_one(
        {"phone": phone},
        {"$set": {"last_order": order, "last_seen": datetime.now(timezone.utc).isoformat()}}
    )
    logger.debug(f"Last order updated for {phone}")

def get_or_create_customer(phone: str, name: str) -> dict:
    customer = get_customer(phone)
    if customer:
        update_last_seen(phone)
        return customer
    return create_customer(phone, name)