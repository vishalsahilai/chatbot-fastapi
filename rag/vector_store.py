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

def _ensure_index_exists():

    pc = _get_pinecone_client()
    existing = [i.name for i in pc.list_indexes()]

    if settings.pinecone_index_name not in existing:
        logger.info(f"Creating Pinecone index: {settings.pinecone_index_name}")
        pc.create_index(
            name=settings.pinecone_index_name,
            dimension=384,  # Dimension of the embeddings
            metric="cosine",
            serverless=ServerlessSpec(
                cloud="aws",
                region="us-east-1"
            )
                
        )
        logger.info("Pinecone index created successfully.")
    else:
        logger.info(f"Pinecone index '{settings.pinecone_index_name}' already exists.")
