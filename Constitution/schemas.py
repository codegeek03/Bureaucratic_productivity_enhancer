from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class QuestionRequest(BaseModel):
    question: str

class Source(BaseModel):
    page: int

class QuestionResponse(BaseModel):
    answer: str
    sources: List[Source]
    timestamp: datetime

class UploadPDFResponse(BaseModel):
    message: str
    file_name: str
    chunks_created: int

class ErrorResponse(BaseModel):
    error: str
    timestamp: datetime