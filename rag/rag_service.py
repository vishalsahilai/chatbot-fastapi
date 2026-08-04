from rag.vector_store import retrieve_context
from utils.logger import logger

def get_rag_context(query: str) -> str:
    logger.debug(f"RAG query: {query[:60]}...")

    context_keywords = ["phone", "number", "contact", "whatsapp", "call", "address", "location", "hours"]
    if any(word in query.lower() for word in context_keywords):
        query = "restaurant phone number whatsapp contact details location hours"

    # Retrieve relevant chunks
    raw_context = retrieve_context(query)

    if not raw_context:
        logger.debug("No context retrieved from Pinecone.")
        return ""

    # Format for LLM injection
    formatted = (
        "-----------------------------------------\n"
        "Retrieved Context:\n"
        "-----------------------------------------\n"
        f"{raw_context}\n"
        "Use the above information to answer the user's question accurately.\n"
        "Only use facts from the above — do not make up any information.\n"
    )

    logger.debug(f"RAG context ready ({len(formatted)} characters)")
    return formatted