from pymongo import MongoClient
from pymongo.database import Database
from config.settings import settings
from utils.logger import logger

_client: MongoClient = None
_db: Database = None


def get_db() -> Database:
    global _client, _db
    if _db is None:
        _client = MongoClient(settings.mongodb_uri)
        _db = _client["sadabahar"]
        logger.info("MongoDB connected.")
    return _db


def close_db():
    global _client, _db
    if _client:
        _client.close()
        _client = None
        _db = None
        logger.info("MongoDB disconnected.")