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

# Save chunks locally to see how PDF was split
def save_chunks_locally(chunks):
    output = []
    for i, chunk in enumerate(chunks):
        output.append({
            "chunk_id": i,
            "content": chunk.page_content,
            "metadata": chunk.metadata
        })
    
    with open("data/chunks_preview.json", "w") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    
    print(f" Saved {len(chunks)} chunks to data/chunks_preview.json")
