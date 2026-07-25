MENU: dict = {
    "pizza":[
        "Margherita",
        "Pepperoni",
    ],
    "burger": [
        "Zinger Burger",
        "Beef Burger",
    ],
    "drinks": [
        "Coca-Cola",
        "Mango Lassi",
        "Mineral Water",
    ],
    "sides": [
        "Garlic Bread",
        "Coleslaw",
        "French Fries",
    ],
    "desserts": [
        "Chocolate Brownie",
        "Gulab Jamun",
    ],
}

def get_manu_as_text() -> str:
    """
    Returns the menu formatted as a readable string
    for injection into the system prompt.  
    """
    lines = ["SADABAHAR RESTAURANT MENU:", ""]
    for category, items in MENU.items():
        lines.append(f "{category.upper()}")
        for item in items:
            lines.append(f"  -{item}")
        lines.append("")
    return "\n".join(lines)