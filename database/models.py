from database.mongodb import get_db

def customers_col():
    return get_db()["customers"]

def sessions_col():
    return get_db()["sessions"]
 
 
def orders_col():
    return get_db()["orders"]