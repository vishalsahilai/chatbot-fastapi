import json
import re
from tenacity import retry, stop_after_attempt, wait_exponential
from utils.logger import logger


@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=1, max=10),
)
async def summarize_conversation(
    user_message: str,
    bot_response: str,
    llm_chain,
) -> dict:
    bot_response_clean = re.sub(r'\{.*?"order_ready".*?\}', '', bot_response, flags=re.DOTALL).strip()

    summarization_prompt = f"""
You are a conversation summarizer for a restaurant chatbot system.

Summarize the following exchange in strict JSON format with exactly these three keys:
- "user_intent"  : A brief description of what the user wanted or asked (1 sentence).
- "bot_response" : A brief summary of what the bot replied (1-2 sentences).
- "context"      : Any useful context that should be remembered for future turns.

Exchange to summarize:
USER: {user_message}
BOT: {bot_response_clean}

Respond ONLY with valid JSON. No preamble, no markdown, no explanation.
Example format:
{{
  "user_intent": "User asked about available pizzas.",
  "bot_response": "Bot listed Margherita and Pepperoni as available options.",
  "context": "User is interested in pizza. May want to place an order."
}}
""".strip()

    try:
        raw = await llm_chain.ainvoke(summarization_prompt)
        if isinstance(raw.content, list):
            raw_text = " ".join(
                block.get("text", "") if isinstance(block, dict) else str(block)
                for block in raw.content
            )
        else:
            raw_text = raw.content if hasattr(raw, "content") else str(raw)

        clean = raw_text.strip()
        if clean.startswith("```"):
            clean = clean.split("```")[1]
            if clean.startswith("json"):
                clean = clean[4:]
        clean = clean.strip()

        summary = json.loads(clean)

        required_keys = {"user_intent", "bot_response", "context"}
        if not required_keys.issubset(summary.keys()):
            raise ValueError(f"Summary missing keys: {required_keys - summary.keys()}")

        logger.debug(f"Summary generated: {summary}")
        return summary

    except Exception as e:
        logger.warning(f"Summarization failed ({e}), using fallback summary.")
        return _fallback_summary(user_message, bot_response_clean)


def _fallback_summary(user_message: str, bot_response: str) -> dict:
    return {
        "user_intent": user_message[:150],
        "bot_response": bot_response[:150],
        "context": "Summary auto-generated due to LLM failure.",
    }