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

def main():
    logger.info("=" * 50)
    logger.info("Sadabahar Restaurant — PDF Ingestion")
    logger.info("=" * 50)

    try:
        # Step 1: Load and chunk PDF
        logger.info("Step 1: Loading and chunking PDF...")
        chunks = load_and_split_pdf()
        logger.info(f"✅ PDF loaded — {len(chunks)} chunks created.")

        # Save chunks locally ← ADD THIS
        save_chunks_locally(chunks)

        # Step 2: Ingest into ChromaDB
        logger.info("Step 2: Ingesting into ChromaDB...")
        ingest_documents(chunks)
        logger.info("✅ ChromaDB populated successfully.")

        logger.info("=" * 50)
        logger.info("✅ Ingestion complete! RAG system is ready.")
        logger.info("You can now run: python -m uvicorn main:app --reload")
        logger.info("=" * 50)

    except FileNotFoundError as e:
        logger.error(f"❌ {e}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"❌ Ingestion failed: {e}")
        sys.exit(1)

