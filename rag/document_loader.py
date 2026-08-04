import os
from langchain.comunity.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from utils.logger import logger