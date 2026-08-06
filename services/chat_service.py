import json
from fastapi import HTTPException
from memory.memory_manager import (
    get_session, save_session, increment_message_count,
    append_summary, set_last_messages, update_order_state, reset_order_state,
)
from memory.context_builder import get_context_for_llm
from memory.summarizer import summarize_conversation
from services.llm_service import safe_invoke_llm, get_summarizer_llm
from services.customer_service import get_customer, update_last_seen
from services.order_service import process_order
from rag.rag_service import get_rag_context
from prompts.system_prompt import build_system_prompt
from utils.menu import is_menu_request, get_formatted_menu
from utils.logger import logger


def _parse_order_from_response(response: str) -> dict | None:
    """
    Try to parse structured order JSON from LLM response.
    LLM returns JSON block when order is ready.
    """
    try:
        start = response.find("{")
        end = response.rfind("}") + 1
        if start == -1 or end == 0:
            return None
        json_str = response[start:end]
        data = json.loads(json_str)
        if data.get("order_ready") is True:
            return data
        return None
    except Exception:
        return None


def _extract_display_message(response: str) -> str:
    """Extract only the human-readable message from LLM response."""
    try:
        start = response.find("{")
        if start == -1:
            return response
        return response[:start].strip()
    except Exception:
        return response


async def process_chat(session_id: str, user_message: str, phone: str = "") -> dict:

    # ── Menu shortcut — skip RAG entirely ────────────────────────
    if is_menu_request(user_message):
        menu_response = f"Here's our complete menu! 🍽️\n\n{get_formatted_menu()}"
        session = get_session(session_id, phone=phone)
        session = increment_message_count(session)
        session = set_last_messages(session, user_message, menu_response)
        save_session(session_id, session)
        return {
            "session_id": session_id,
            "response": menu_response,
            "message_count": session["message_count"],
        }

    import re

    SKIP_RAG_PATTERNS = [
        r"^\d{10,15}$",                    # phone numbers
        r"^[^@\s]+@[^@\s]+\.[^@\s]+$",   # emails
        r"^(yes|no|ok|okay|confirm|done|nothing|else|thanks|sure|yep|nope|hi|hello|salam)$",
        r"^[\w\s,.-]{3,50}$",             # short addresses
    ]

    def _should_skip_rag(message: str) -> bool:
        msg = message.lower().strip()
        return any(re.match(p, msg, re.IGNORECASE) for p in SKIP_RAG_PATTERNS)

    # ── Load customer ─────────────────────────────────────────────
    customer_name = ""
    last_order = None

    if phone:
        customer = get_customer(phone)
        if customer:
            customer_name = customer.get("name", "")
            last_order = customer.get("last_order")
            update_last_seen(phone)

    #  Load session 
    session = get_session(session_id, phone=phone, name=customer_name)
    if not customer_name:
        customer_name = session.get("name", "")

    logger.info(f"[{session_id}] Message #{session['message_count'] + 1}: '{user_message[:60]}'")

    #  Build dynamic system prompt 
    system_prompt = build_system_prompt(
        customer_name=customer_name,
        last_order=last_order if session["message_count"] == 0 else None,
    )

    #  Get RAG context 
    rag_context = "" if _should_skip_rag(user_message) else get_rag_context(user_message)

    #  Build memory context 
    memory_context = get_context_for_llm(session, user_message)
    full_context = f"{rag_context}\n\n{memory_context}" if rag_context else memory_context

    #  Invoke LLM 
    try:
        raw_response = await safe_invoke_llm(full_context, system_prompt=system_prompt)
    except Exception as e:
        logger.error(f"[{session_id}] LLM failure: {e}")
        raise HTTPException(status_code=503, detail="LLM service is temporarily unavailable.")

    #  Check if order is ready 
    order_data = _parse_order_from_response(raw_response)
    display_message = _extract_display_message(raw_response)

    if order_data:
        logger.info(f"[{session_id}] Order detected — processing...")
        try:
            order_payload = {
                "session_id": session_id,
                "phone": order_data.get("phone", phone),
                "name": order_data.get("name", customer_name),
                "email": order_data.get("email", ""),
                "address": order_data.get("address", ""),
                "items": order_data.get("items", []),
                "total": order_data.get("total", 0),
            }
            order_result = await process_order(order_payload)
            display_message = (
                f"✅ Order confirmed! Your order ID is *{order_result['order_id']}*.\n"
                f"A confirmation email has been sent to {order_payload['email']}.\n"
                f"Estimated delivery: {order_result['estimated_time']} 🍕"
            )
            session = reset_order_state(session)
            logger.info(f"[{session_id}] Order {order_result['order_id']} placed successfully.")
        except Exception as e:
            logger.error(f"[{session_id}] Order processing failed: {e}")
            display_message = "I'm sorry, there was an issue placing your order. Please try again or call us at +92 336 6874263."

    #  Update memory 
    session = increment_message_count(session)

    if session["message_count"] >= 2:
        try:
            summary = await summarize_conversation(
                user_message=user_message,
                bot_response=display_message,
                llm_chain=get_summarizer_llm(),
            )
            session = append_summary(session, summary)
        except Exception as e:
            logger.warning(f"[{session_id}] Summarization skipped: {e}")

    session = set_last_messages(session, user_message, display_message)

    if customer_name and not session.get("name"):
        session["name"] = customer_name
    if phone and not session.get("phone"):
        session["phone"] = phone

    save_session(session_id, session)

    return {
        "session_id": session_id,
        "response": display_message,
        "message_count": session["message_count"],
    }