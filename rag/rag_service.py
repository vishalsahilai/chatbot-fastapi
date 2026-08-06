from rag.vector_store import retrieve_context
from utils.logger import logger


def format_context(context: str) -> str:
    """
    Formats retrieved RAG context before injecting into the LLM prompt.
    """
    if not context:
        return ""

    return (
        "-----------------------------------------\n"
        "Retrieved Context:\n"
        "-----------------------------------------\n"
        f"{context}\n\n"
        "Instructions:\n"
        "- Use ONLY the information above to answer the user's question.\n"
        "- Do NOT invent or assume information.\n"
        "- If the answer is not present, politely state that the information is unavailable.\n"
    )


def get_rag_context(query: str) -> str:
    """
    Retrieves relevant restaurant information from Pinecone.
    Performs specialized retrieval for menu/order queries and
    contact/location queries.
    """

    logger.debug(f"RAG Query: {query}")

    query_lower = query.lower()

    # ----------------------------------------------------
    # Contact / Location queries
    # ----------------------------------------------------
    contact_keywords = [
        "phone",
        "number",
        "contact",
        "whatsapp",
        "call",
        "address",
        "location",
        "hours",
        "timing",
        "open",
        "close",
    ]

    if any(keyword in query_lower for keyword in contact_keywords):
        logger.debug("Detected contact/location query.")

        search_query = (
            "restaurant phone number whatsapp contact "
            "address location operating hours"
        )

        context = retrieve_context(search_query)

        if not context:
            logger.debug("No contact information found.")
            return ""

        logger.debug("Contact information retrieved successfully.")
        return format_context(context)

    # ----------------------------------------------------
    # Menu / Order queries
    # ----------------------------------------------------
    menu_keywords = [
        "order",
        "price",
        "cost",
        "deal",
        "family",
        "puri",
        "biryani",
        "karahi",
        "pizza",
        "burger",
        "menu",
        "dish",
        "food",
    ]

    if any(keyword in query_lower for keyword in menu_keywords):
        logger.debug("Detected menu/order query.")

        contexts = []

        context1 = retrieve_context(query)
        if context1:
            contexts.append(context1)

        context2 = retrieve_context(f"menu prices {query}")
        if context2:
            contexts.append(context2)

        context3 = retrieve_context("complete restaurant menu with prices")
        if context3:
            contexts.append(context3)

        if not contexts:
            logger.debug("No menu information found.")
            return ""

        combined_context = "\n\n".join(dict.fromkeys(contexts))

        logger.debug(
            f"Retrieved {len(contexts)} menu context(s). "
            f"Length={len(combined_context)}"
        )

        return format_context(combined_context)

    # ----------------------------------------------------
    # General Retrieval
    # ----------------------------------------------------
    logger.debug("Performing general semantic retrieval.")

    context = retrieve_context(query)

    if not context:
        logger.debug("No relevant context found.")
        return ""

    logger.debug(f"Retrieved context length: {len(context)}")
    return format_context(context)