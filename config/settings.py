from typing import list
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8", #Read the .env file using UTF-8 encoding/ UTF-8 supports all characters including special symbols, emojis, other languages
        case_sensitive=False,
    )