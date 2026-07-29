from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from tenacity import retry, stop_after_attempt, wait_exponential, RetryError

from config.settings import settings
from prompts.system_prompt import SYSTEM_PROMPT
from utils.logger import logger