from fastapi import HTTPException
from memory.memory_manager import (
    get_session, save_session, increment_message_count,
    append_summary, set_last_messages,
)
from memory.context_builder import get_context_for_llm
from memory.summarizer import summarize_conversation
from services.llm_service import safe_invoke_llm, get_summarizer_llm
from services.customer_service import get_customer, get_or_create_customer
from rag.rag_service import get_rag_context
from prompts.system_prompt import build_system_prompt
from utils.menu import is_menu_request, get_formatted_menu
from utils.logger import logger


async def process_chat(session_id: str, user_message: str, phone: str = "") -> dict:


    # Menu shortcut - Skip RAG and LLM completely

    if is_menu_request(user_message):
        menu_response = (
            f"Here's our complete menu! 🍽️\n\n"
            f"{get_formatted_menu()}"
        )

        session = get_session(session_id, phone=phone)
        session = increment_message_count(session)
        session = set_last_messages(session, user_message, menu_response)
        save_session(session_id, session)

        return {
            "session_id": session_id,
            "response": menu_response,
            "message_count": session["message_count"],
        }


    # Normal chatbot flow

    # Load customer if phone provided
    customer = None
    customer_name = ""
    last_order = None

    if phone:
        customer = get_customer(phone)
        if customer:
            customer_name = customer.get("name", "")
            last_order = customer.get("last_order")

    # Load session
    session = get_session(session_id, phone=phone, name=customer_name)

    # Use name from session if not from customer lookup
    if not customer_name:
        customer_name = session.get("name", "")

    logger.info(
        f"[{session_id}] Message #{session['message_count'] + 1}: '{user_message[:60]}'"
    )

    # Build dynamic system prompt
    system_prompt = build_system_prompt(
        customer_name=customer_name,
        last_order=last_order if session["message_count"] == 0 else None,
    )

    # Get RAG context
    rag_context = get_rag_context(user_message)

    # Build memory context
    memory_context = get_context_for_llm(session, user_message)

    # Combine contexts
    full_context = (
        f"{rag_context}\n\n{memory_context}"
        if rag_context
        else memory_context
    )

    # Invoke LLM
    try:
        bot_response = await safe_invoke_llm(
            full_context,
            system_prompt=system_prompt,
        )
    except Exception as e:
        logger.error(f"[{session_id}] LLM failure: {e}")
        raise HTTPException(
            status_code=503,
            detail="LLM service is temporarily unavailable.",
        )

    # Update memory
    session = increment_message_count(session)

    if session["message_count"] >= 2:
        try:
            summary = await summarize_conversation(
                user_message=user_message,
                bot_response=bot_response,
                llm_chain=get_summarizer_llm(),
            )
            session = append_summary(session, summary)
        except Exception as e:
            logger.warning(
                f"[{session_id}] Summarization skipped: {e}"
            )

    session = set_last_messages(
        session,
        user_message,
        bot_response,
    )

    # Store customer name in session
    if customer_name and not session.get("name"):
        session["name"] = customer_name

    save_session(session_id, session)

    return {
        "session_id": session_id,
        "response": bot_response,
        "message_count": session["message_count"],
    }