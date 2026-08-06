"""
Sadabahar Restaurant Chatbot — Email Service
Sends order confirmation emails via Resend API.
Free tier: 3000 emails/month — more than enough.
"""

import resend
from config.settings import settings
from utils.logger import logger


def _build_email_body(order: dict) -> str:
    """Builds HTML email body for order confirmation."""
    items_html = "".join(
        f"<tr><td>{i['name']} ({i.get('size', '')})</td><td>x{i['qty']}</td><td>PKR {i['price']}</td></tr>"
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


async def send_confirmation_email(order: dict) -> None:
    """
    Sends order confirmation email via Resend API.

    Args:
        order: Order dict containing email, name, order_id, items, total.

    Returns:
        None — logs success or skips if no email provided.
    """
    # Skip if no email provided
    if not order.get("email"):
        logger.warning(f"[{order.get('order_id')}] No email provided — skipping confirmation.")
        return

    try:
        # Set API key
        resend.api_key = settings.resend_api_key

        # Send email
        response = resend.Emails.send({
            "from": "Sadabahar Restaurant <onboarding@resend.dev>",
            "to": order["email"],
            "subject": f"Order Confirmed — Sadabahar Restaurant 🍕 ({order['order_id']})",
            "html": _build_email_body(order),
        })

        logger.info(f"[{order['order_id']}] Confirmation email sent to {order['email']} — ID: {response['id']}")

    except Exception as e:
        logger.error(f"[{order['order_id']}] Email sending failed: {e}")