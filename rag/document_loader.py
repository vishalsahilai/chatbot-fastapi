import os
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from utils.logger import logger

# Path to the PDF file
PDF_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "Sadabahar_Restaurant.pdf")

# Chunk settings
CHUNK_SIZE = 500        # characters per chunk
CHUNK_OVERLAP = 100     # overlap between chunks for context continuity

def load_and_split_pdf() -> list:
    """
    Load the restaurant PDF and split it into chunks.
    
    Returns:
        list of Document object with text chunks.
        
    Raises:
        FileNotFoundError If the PDF file does not exist.
    """
    if not os.path.exists(PDF_PATH):
        raise FileNotFoundError(
            f"PDF file not found at {PDF_PATH}\n"
            f"Please place 'Sadabahar_Restaurant.pdf' in the 'data' directory."
        )
    logger.info(f"Loading PDF from: {PDF_PATH}")

#load PDF
    loader = PyPDFLoader(PDF_PATH)
    pages = loader.load()
    logger.info(f"PDF Loaded {len(pages)} pages found.")

#split into chunks
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=["\n\n", "\n", " .", "!","?", ",", " "]
    )

    chunks = splitter.split_documents(pages)
    logger.info(f"PDF Split into {len(chunks)} chunks.")
    return chunks