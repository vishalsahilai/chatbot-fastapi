def get_formatted_menu() -> str:
    return """
🍕 *PIZZAS*
- Margherita — Small PKR 750 | Medium PKR 1,250 | Large PKR 1,750
- Pepperoni — Small PKR 900 | Medium PKR 1,450 | Large PKR 2,050
- Chicken Fajita — Small PKR 950 | Medium PKR 1,500 | Large PKR 2,100
- Chicken Tikka — Small PKR 950 | Medium PKR 1,500 | Large PKR 2,100
- BBQ Chicken — Small PKR 1,000 | Medium PKR 1,600 | Large PKR 2,250
- Supreme — Small PKR 1,100 | Medium PKR 1,750 | Large PKR 2,500
- Veggie — Small PKR 800 | Medium PKR 1,350 | Large PKR 1,900
- Cheese Lovers — Small PKR 950 | Medium PKR 1,500 | Large PKR 2,100

🍔 *BURGERS*
- Zinger Burger — Single PKR 520 | Double PKR 690
- Crispy Chicken — Single PKR 500 | Double PKR 670
- Grilled Chicken — Single PKR 560 | Double PKR 740
- BBQ Beef — Single PKR 680 | Double PKR 890
- Cheese Burger — Single PKR 550 | Double PKR 720

🍟 *SIDES*
- French Fries — Regular PKR 220 | Large PKR 350
- Garlic Bread — Regular PKR 280 | Large PKR 420
- Coleslaw — Regular PKR 180 | Large PKR 280
- Chicken Nuggets — 6pcs PKR 420 | 12pcs PKR 720
- Onion Rings — Regular PKR 260 | Large PKR 420
- Mozzarella Sticks — Regular PKR 550 | Large PKR 850

🥤 *DRINKS*
- Coca-Cola — Small PKR 120 | Large PKR 220
- Sprite — Small PKR 120 | Large PKR 220
- Mango Lassi — Small PKR 260 | Large PKR 380
- Mint Margarita — Small PKR 260 | Large PKR 380
- Fresh Orange Juice — Small PKR 350 | Large PKR 500
- Mineral Water — Small PKR 80 | Large PKR 150

🍰 *DESSERTS*
- Chocolate Brownie — PKR 320
- Gulab Jamun (2pcs) — PKR 220
- Ice Cream Sundae — PKR 350
- Chocolate Lava Cake — PKR 480
- Cheesecake Slice — PKR 550

🍗 *BBQ*
- Chicken Tikka — PKR 520
- Chicken Boti — PKR 650
- Malai Boti — PKR 720
- Mix BBQ Platter — PKR 2,350

🍛 *PAKISTANI*
- Chicken Biryani — PKR 420
- Chicken Karahi Half — PKR 1,250 | Full PKR 2,350
- Mutton Karahi Half — PKR 2,100 | Full PKR 3,950
- Nihari — PKR 620
- Haleem — PKR 380

🍝 *PASTA*
- Alfredo Pasta — PKR 720
- White Sauce Pasta — PKR 680
- Red Sauce Pasta — PKR 650

🥪 *SANDWICHES & WRAPS*
- Chicken Club Sandwich — PKR 620
- Chicken Wrap — PKR 520

🍳 *BREAKFAST (9AM-12PM)*
- Halwa Puri — PKR 450
- Omelette Breakfast — PKR 350
- Special Breakfast Platter — PKR 850

👨‍👩‍👧‍👦 *FAMILY DEALS*
- Family Deal 1: Large Pizza + Large Fries + 1.5L Drink — PKR 2,450
- Family Deal 2: 2 Zingers + Large Fries + 2 Drinks — PKR 2,150
- Family Deal 3: Half Karahi + 4 Naan + Salad + 1.5L Drink — PKR 2,950
- Family BBQ: 2 Tikka + 2 Boti + 2 Seekh + Naan + Salad — PKR 3,850

🎉 *COMBO DEALS*
- Combo 1: Zinger + Fries + Drink — PKR 790
- Combo 2: Beef Burger + Nuggets + Drink — PKR 990
- Combo 3: Medium Pizza + Garlic Bread + Drink — PKR 1,790
- Combo 4: Biryani + Drink + Dessert — PKR 720

*Delivery: PKR 100 (0-3km) | PKR 150 (3-6km) | PKR 250 (6-10km)*
*Min order: PKR 500 | Hours: 9AM-11PM*
""".strip()


MENU_KEYWORDS = [
    "menu", "what do you have", "what do you serve",
    "show me", "full menu", "complete menu", "price list",
    "what can i order", "what's available", "kya hai",
    "manu", "items", "list"
]


def is_menu_request(message: str) -> bool:
    message_lower = message.lower()
    return any(keyword in message_lower for keyword in MENU_KEYWORDS)