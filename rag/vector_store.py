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