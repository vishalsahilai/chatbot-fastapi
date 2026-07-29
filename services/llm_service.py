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