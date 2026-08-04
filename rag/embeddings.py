from langchain_community.embeddings import HuggingFaceEmbeddings
from utils.logger import logger

EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

_embeddings = None