from pymongo import MongoClient
from pymongo.database import Database
from config.settings import settings
from utils.logger import logger

_client: MongoClient = None
_db: Database = None

