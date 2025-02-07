from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import logging
from datetime import datetime
import os

from config import API_TITLE, API_DESCRIPTION, API_VERSION
from schemas import QuestionRequest, QuestionResponse, UploadPDFResponse, ErrorResponse, Source
from vector_store import load_or_create_vector_store
from qa_chain import create_qa_chain
from pdf_loader import load_and_split_pdf

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title=API_TITLE,
    description=API_DESCRIPTION,
    version=API_VERSION,
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize QA system components
try:
    vector_store = load_or_create_vector_store()
    qa_chain = create_qa_chain(vector_store)
    logger.info("QA system initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize QA system: {str(e)}")
    raise

@app.get("/")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow()
    }

@app.post("/api/v1/ask", response_model=QuestionResponse)
async def ask_question(request: QuestionRequest):
    """
    Ask a question about the loaded PDF content
    """
    try:
        logger.info(f"Received question: {request.question}")
        result = qa_chain.invoke({"query": request.question})
        
        sources = [
            Source(page=doc.metadata['page'])
            for doc in result['source_documents']
        ]
        
        response = QuestionResponse(
            answer=result['result'],
            sources=sources,
            timestamp=datetime.utcnow()
        )
        
        logger.info("Successfully generated response")
        return response
        
    except Exception as e:
        logger.error(f"Error processing question: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=ErrorResponse(
                error=f"Failed to process question: {str(e)}",
                timestamp=datetime.utcnow()
            ).dict()
        )

@app.post("/api/v1/upload", response_model=UploadPDFResponse)
async def upload_pdf(file: UploadFile = File(...)):
    """
    Upload a new PDF file and create vector store
    """
    try:
        # Ensure file is PDF
        if not file.filename.lower().endswith('.pdf'):
            raise HTTPException(
                status_code=400,
                detail="Only PDF files are allowed"
            )

        # Save uploaded file temporarily
        temp_path = f"temp_{file.filename}"
        with open(temp_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)

        # Process PDF
        logger.info(f"Processing PDF: {file.filename}")
        chunks = load_and_split_pdf(temp_path)
        vector_store = load_or_create_vector_store(chunks=chunks)
        
        # Clean up temporary file
        os.remove(temp_path)

        return UploadPDFResponse(
            message="PDF processed successfully",
            file_name=file.filename,
            chunks_created=len(chunks)
        )

    except Exception as e:
        logger.error(f"Error processing PDF upload: {str(e)}")
        if os.path.exists(temp_path):
            os.remove(temp_path)
        raise HTTPException(
            status_code=500,
            detail=ErrorResponse(
                error=f"Failed to process PDF: {str(e)}",
                timestamp=datetime.utcnow()
            ).dict()
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)