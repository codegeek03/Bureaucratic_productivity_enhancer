import os
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables
load_dotenv()

# System Information
CURRENT_TIME = "2025-02-07 22:00:01"
CURRENT_USER = "codegeek03"

# API Keys
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")

if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY not found in environment variables")
if not HUGGINGFACE_API_KEY:
    raise ValueError("HUGGINGFACE_API_KEY not found in environment variables")

# Model configurations
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
GROQ_CHAT_MODEL = "llama3-8b-8192"

# API configurations
API_VERSION = "v1"
API_TITLE = "PDF QA System API"
API_DESCRIPTION = "API for querying PDF documents using LangChain and Groq"