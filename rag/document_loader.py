import os
from langchain.comunity.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from utils.logger import logger

# Path to the PDF file
PDF_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "Sadabahar_Restaurant.pdf")

# Chunk settings
CHUNK_SIZE = 500        # characters per chunk
CHUNK_OVERLAP = 100     # overlap between chunks for context continuity