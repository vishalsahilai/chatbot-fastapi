from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage
from tenacity import retry, stop_after_attempt, wait_exponential, RetryError

from config.settings import settings
from prompts.system_prompt import SYSTEM_PROMPT
from utils.logger import logger



# LLM Instance (shared, thread-safe)
_llm = ChatGoogleGenerativeAI(
    model=settings.gemini_model,
    temperature=settings.llm_temperature,
    max_output_tokens=settings.llm_max_tokens,
    google_api_key=settings.google_api_key,
)

# Summarizer LLM (lower temp for consistency)
_summarizer_llm = ChatGoogleGenerativeAI(
    model=settings.gemini_model,
    temperature=0.1,
    max_output_tokens=300,
    google_api_key=settings.google_api_key,
)

def get_llm() -> ChatGoogleGenerativeAI:
    """Returns the main chat LLM instance."""
    return _llm

def get_summarizer_llm() -> ChatGoogleGenerativeAI:
    """Returns the summarizer LLM instance (lower temperature)."""
    return _summarizer_llm

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=1, max=10),
)
async def invoke_llm(user_context: str) -> str:
    """
    Sends a message to the LLM with the system prompt.

    Args:
        user_context : The assembled context string from context_builder.
                       This may include summaries + current user message,
                       or just the raw message depending on the phase.

    Returns:
        The LLM's text response as a string.

    Raises:
        RuntimeError if all retry attempts fail.
    """
    try:
        messages = [
            SystemMessage(content=SYSTEM_PROMPT),
            HumanMessage(content=user_context),
        ]

        response = await _llm.ainvoke(messages)
        # Gemini can return content as a list or a string
        if isinstance(response.content, list):
            reply = " ".join(
                block.get("text", "") if isinstance(block, dict) else str(block)
                for block in response.content
            ).strip()
        else:
            reply = response.content.strip()

        logger.debug(f"Gemini response ({len(reply)} chars): {reply[:100]}...")
        return reply

    except Exception as e:
        logger.error(f"Gemini invocation failed: {e}")
        raise


async def safe_invoke_llm(user_context: str) -> str:
    """
    Wrapper around invoke_llm with top-level error handling.
    Raises HTTPException-friendly errors if all retries fail.
    """
    try:
        return await invoke_llm(user_context)
    except RetryError:
        logger.error("Gemini failed after all retry attempts.")
        raise
    except Exception as e:
        logger.error(f"Unexpected Gemini error: {e}")
        raise