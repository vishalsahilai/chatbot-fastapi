import os
import sys
import json
from dotenv import load_dotenv
load_dotenv()

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from rag.document_loader import load_and_split_pdf
from rag.vector_store import ingest_documents
from utils.logger import logger