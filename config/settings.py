from typing import list
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8", #Read the .env file using UTF-8 encoding/ UTF-8 supports all characters including special symbols, emojis, other languages
        case_sensitive=False,
    )

#LLM
google_api_key: str = "changeme"
gemini_model: str = "gemini-2.5-flast"
llm_temperature: float = 0.7
llm_max_tokens: int = 512 #tokens ≈ roughly 350-400 words

#App
#"development"	Running locally on your machine 
#"staging"	Testing before going live
#"production"	Live app for real users
app_env: str = "development"
app_host: str = "0.0.0.0"
app_port: int = 8000
debug: bool = True

#Memory
memory_backend: str = "both"      # "dict" | "redis"
max_summaries: int = 5