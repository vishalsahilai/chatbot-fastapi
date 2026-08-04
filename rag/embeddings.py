from langchain_community.embeddings import HuggingFaceEmbeddings
from utils.logger import logger

EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

_embeddings = None

def get_embeddings() -> HuggingFaceEmbeddings:
    """
    Returns HuggingFace embeddings instance.
    Lazy initialized — only loads once.
    """
    global _embeddings
    if _embeddings is None:
        logger.info(f"Loading embedding model: {EMBEDDING_MODEL}")
        _embeddings = HuggingFaceEmbeddings(
            model_name=EMBEDDING_MODEL,
            model_kwargs={"device": "cpu"},
            encode_kwargs={"normalize_embeddings": True},
        )
        logger.info("Embedding model loaded successfully.")
    return _embeddings