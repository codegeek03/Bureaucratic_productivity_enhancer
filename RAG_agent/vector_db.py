# Vector store remains mostly the same since it's already using HuggingFace embeddings
import os
os.environ["TOKENIZERS_PARALLELISM"] = "false"

import warnings
warnings.filterwarnings('ignore', category=DeprecationWarning)

import logging
from langchain_chroma import Chroma
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
import chromadb

# Set up logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

class VectorStore:
    def __init__(self, model_name="all-MiniLM-L6-v2", persist_directory="./chroma_db", dry_run=False):
        """Initialize the vector store with the specified embedding model."""
        self.dry_run = dry_run
        logging.debug(f"[__init__] Initializing VectorStore with model: {model_name}, dry_run: {self.dry_run}")
        self.embedding_function = HuggingFaceEmbeddings(model_name=model_name)
        self.persist_directory = persist_directory
        
        if not self.dry_run:
            if os.path.exists(persist_directory):
                try:
                    self.db = Chroma(
                        persist_directory=persist_directory,
                        embedding_function=self.embedding_function,
                        client_settings=chromadb.config.Settings(
                            anonymized_telemetry=False,
                            is_persistent=True
                        )
                    )
                    logging.info("[__init__] Loaded existing vector store from disk")
                except Exception as e:
                    logging.error(f"[__init__] Error loading existing vector store: {e}")
                    self.db = None
            else:
                self.db = None
        else:
            self.db = None
            logging.info("[__init__] Dry run mode - skipping DB load")

    # Rest of the VectorStore class methods remain the same