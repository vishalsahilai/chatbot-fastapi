"""
Sadabahar Restaurant Chatbot — Conversation Summarizer
 
Calls the LLM to generate a structured summary of a single user↔bot exchange.
Each summary captures:
  - user_intent  : what the user was trying to accomplish
  - bot_response : what the bot said (condensed)
  - context      : any important context for future turns
"""
import json
from tenacity import retry, stop_after_attempt, wait_exponential

from config.settings import settings
from utils.logger import logger

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=1, max=10),
)