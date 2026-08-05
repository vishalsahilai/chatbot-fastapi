from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage
from tenacity import retry, stop_after_attempt, wait_exponential, RetryError
from config.settings import settings
from prompts.system_prompt import build_system_prompt
from utils.logger import logger

API_KEYS = [k for k in [
    settings.google_api_key_1,
    settings.google_api_key_2,
    settings.google_api_key_3,
    settings.google_api_key_4,
] if k]

_current_key_index = 0


def _get_current_key() -> str:
    return API_KEYS[_current_key_index]


def _rotate_key():
    global _current_key_index
    _current_key_index = (_current_key_index + 1) % len(API_KEYS)
    logger.warning(f"Rotated to API key index: {_current_key_index}")


def _build_llm(api_key: str, temperature: float = None, max_tokens: int = None):
    return ChatGoogleGenerativeAI(
        model=settings.gemini_model,
        temperature=temperature or settings.llm_temperature,
        max_output_tokens=max_tokens or settings.llm_max_tokens,
        google_api_key=api_key,
    )


def get_llm():
    return _build_llm(_get_current_key())


def get_summarizer_llm():
    return _build_llm(_get_current_key(), temperature=0.1, max_tokens=300)


async def invoke_llm(user_context: str, system_prompt: str = None) -> str:
    if not API_KEYS:
        raise RuntimeError("No API keys configured.")

    prompt = system_prompt or build_system_prompt()
    last_error = None

    for _ in range(len(API_KEYS)):
        try:
            llm = _build_llm(_get_current_key())
            messages = [
                SystemMessage(content=prompt),
                HumanMessage(content=user_context),
            ]
            response = await llm.ainvoke(messages)

            if isinstance(response.content, list):
                reply = " ".join(
                    block.get("text", "") if isinstance(block, dict) else str(block)
                    for block in response.content
                ).strip()
            else:
                reply = response.content.strip()

            return reply

        except Exception as e:
            error_msg = str(e).lower()
            if any(k in error_msg for k in ["quota", "rate limit", "429", "resource exhausted"]):
                logger.warning(f"Key {_current_key_index} quota hit. Rotating...")
                _rotate_key()
                last_error = e
            else:
                logger.error(f"LLM error: {e}")
                raise

    raise RuntimeError("All Gemini API keys exhausted.") from last_error


async def safe_invoke_llm(user_context: str, system_prompt: str = None) -> str:
    try:
        return await invoke_llm(user_context, system_prompt=system_prompt)
    except Exception as e:
        logger.error(f"safe_invoke_llm failed: {e}")
        raise