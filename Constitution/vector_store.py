from langchain_chroma import Chroma
from embeddings import get_embeddings

def load_or_create_vector_store(chunks=None, persist_directory="db"):
    """
    Load existing vector store or create a new one if chunks are provided
    """
    embeddings = get_embeddings()
    
    if chunks:
        # Create new vector store if chunks are provided
        vector_store = Chroma.from_documents(
            documents=chunks,
            embedding=embeddings,
            persist_directory=persist_directory
        )
    else:
        # Load existing vector store if no chunks provided
        vector_store = Chroma(
            persist_directory=persist_directory,
            embedding_function=embeddings
        )
    
    return vector_store