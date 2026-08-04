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
    """Create Pinecone index if it doesn't exist."""
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

def get_vector_store() -> PineconeVectorStore:
    """Returns Pinecone vector store instance."""
    global _vector_store
    if _vector_store is None:
        _ensure_index_exists()
        logger.info("Creating Pinecone vector store...")
        _vector_store = PineconeVectorStore(
            index_name=settings.pinecone_index_name,
            embedding=get_embeddings(),
            pinecone_api_key=settings.pinecone_api_key or os.getenv("PINECONE_API_KEY")
        )
        logger.info("Pinecone vector store connected successfully.")
    return _vector_store