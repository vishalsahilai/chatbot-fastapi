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
