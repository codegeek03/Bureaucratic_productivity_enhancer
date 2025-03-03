import logging
from vector_db import VectorStore
from llm_utils import LocalRAG
import time

def main(user_query, initialize=False, pdf_path=None, dry_run=False):
    logging.debug(f"[main] Starting process with query: {user_query[:100]}...")
    if dry_run:
        logging.info("[main] Running in dry run mode")
    
    # Initialize vector store
    vector_store = VectorStore(persist_directory="./chroma_db")
    
    # Initialize LocalRAG
    rag = LocalRAG()
    
    if initialize and pdf_path:
        logging.info(f"[main] Initializing with PDF: {pdf_path}")
        vector_store.initialize_from_pdf(pdf_path)
        return "PDF processed and ready for questions!"
    elif not vector_store.db and not initialize:
        logging.error("[main] No vector store found")
        return "Error: Vector store not initialized. Please provide a PDF file first."
    elif initialize:
        logging.error("[main] PDF path not provided for initialization")
        return "Please provide a PDF file to initialize the system."
    
    logging.debug("[main] Starting query processing")
    
    # Get relevant context from vector store
    context = vector_store.search(user_query)
    
    # Generate response using local LLM
    response = rag.process_query(user_query, context)
    
    # Assess confidence
    if rag.assess_confidence(response):
        logging.info("[main] Returning high-confidence response")
        return response
    
    # If confidence is low, synthesize a better response
    logging.debug("[main] Confidence low, synthesizing better response")
    synthesized_response = rag.synthesize_information(response)
    
    logging.info("[main] Returning synthesized response")
    return synthesized_response