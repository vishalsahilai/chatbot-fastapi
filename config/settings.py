from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8", #Read the .env file using UTF-8 encoding/ UTF-8 supports all characters including special symbols, emojis, other languages
        case_sensitive=False,
    )

    # (Gemini) 
    google_api_key_1: str = ""
    google_api_key_2: str = ""
    google_api_key_3: str = ""
    gemini_model: str = "gemini-2.5-flash"
    llm_temperature: float = 0.7
    llm_max_tokens: int = 512

    #App
    app_env: str = "development"
    app_host: str = "0.0.0.0"
    app_port: int = 8000
    debug: bool = True

    # MongoDB
    mongodb_uri: str = "mongodb://localhost:27017"

    # Pinecone
    pinecone_api_key: str = ""
    pinecone_index_name: str = "sadabahar-restaurant"

    # Google Sheets
    google_sheets_id: str = ""
    google_service_account_json: str = ""


    #CORS 
    cors_origins: List[str] = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:5500",
        "http://127.0.0.1:5500",
    ]


# Singleton instance used across the app
settings = Settings()
