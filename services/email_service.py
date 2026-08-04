import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config.settings import settings
from utils.logger import logger

def _build_email_body(order: dict) -> str:
    items_html = "".join(
        f"<tr><td>{i['name']} ({i.get('size','')})</td><td>x{i['qty']}</td><td>PKR {i['price']}</td></tr>"
        for i in order["items"]
    )
    return f"""
    <html><body>
    <h2>Order Confirmed — Sadabahar Restaurant 🍕</h2>
    <p>Dear {order['name']},</p>
    <p>Your order <strong>{order['order_id']}</strong> has been confirmed!</p>
    <table border="1" cellpadding="8">
      <tr><th>Item</th><th>Qty</th><th>Price</th></tr>
      {items_html}
    </table>
    <p><strong>Total: PKR {order['total']}</strong></p>
    <p>Estimated delivery: 30-45 minutes</p>
    <p>📞 +92 336 6874263</p>
    <p>Thank you for ordering from Sadabahar Restaurant!</p>
    </body></html>
    """

async def send_confirmation_email(order: dict):
    if not order.get("email"):
        logger.warning("No email provided — skipping confirmation.")
        return
 
    msg = MIMEMultipart("alternative")
    msg["Subject"] = f"Order Confirmed — Sadabahar Restaurant 🍕 ({order['order_id']})"
    msg["From"] = settings.email_from
    msg["To"] = order["email"]
    msg.attach(MIMEText(_build_email_body(order), "html"))
 
    with smtplib.SMTP(settings.email_host, settings.email_port) as server:
        server.starttls()
        server.login(settings.email_username, settings.email_password)
        server.sendmail(settings.email_from, order["email"], msg.as_string())
 
    logger.info(f"Confirmation email sent to {order['email']}")