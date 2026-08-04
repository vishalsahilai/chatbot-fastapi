import os 
import hashlib
from dotenv import load_dotenv

load_dotenv()
from pinecone import Pinecone, ServerlessSpec
from langchain_pinecone import PineconeVectorStore
from rag.embeddings import get_embeddings
from config.settings import settings
from utils.logger import logger

_vector_store = None

def _get_pinecone_client():
    """Initialize Pinecone client."""
    api_key =  settings.pinecone_api_key or os.getenv("PINECONE_API_KEY")
    return Pinecone(api_key=api_key)