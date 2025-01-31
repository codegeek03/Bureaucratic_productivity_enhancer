from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field
from datetime import datetime
import pytz
from typing import Optional
from translator import translate

app = FastAPI(
    title="Language Translation API",
    description="API for translating between English and Hindi",
    version="1.0.0"
)

# Mount static files and templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

class TranslationRequest(BaseModel):
    text: str = Field(..., min_length=1, description="Text to be translated")
    source_lang: str = Field(..., description="Source language (English or Hindi)")
    target_lang: str = Field(..., description="Target language (English or Hindi)")
    country: str = Field(default="India", description="Country context for translation")

    class Config:
        schema_extra = {
            "example": {
                "text": "Hello, how are you?",
                "source_lang": "English",
                "target_lang": "Hindi",
                "country": "India"
            }
        }

class TranslationResponse(BaseModel):
    status: str
    translated_text: str
    source_lang: str
    target_lang: str
    timestamp: str
    detected_language: Optional[str] = None

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    try:
        current_time = datetime.now(pytz.UTC).strftime('%Y-%m-%d %H:%M:%S')
        return templates.TemplateResponse(
            "index.html",
            {
                "request": request,
                "current_time": current_time,
                "user": "codegeek03",
                "default_source": "English",
                "default_target": "Hindi"
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Template rendering error: {str(e)}")

@app.post("/translate/", response_model=TranslationResponse)
async def translate_text(request: TranslationRequest):
    try:
        # Validate language combination
        valid_languages = {"English", "Hindi"}
        
        # Convert language strings to title case for consistency
        source_lang = request.source_lang.title()
        target_lang = request.target_lang.title()

        # Validate languages
        if source_lang not in valid_languages or target_lang not in valid_languages:
            raise HTTPException(
                status_code=400,
                detail={
                    "error": "Invalid language combination",
                    "message": "Only English and Hindi are supported",
                    "valid_languages": list(valid_languages)
                }
            )
        
        if source_lang == target_lang:
            raise HTTPException(
                status_code=400,
                detail={
                    "error": "Invalid language pair",
                    "message": "Source and target languages must be different"
                }
            )

        # Validate text content
        if not request.text.strip():
            raise HTTPException(
                status_code=400,
                detail={
                    "error": "Empty text",
                    "message": "Please provide text to translate"
                }
            )

        # Perform translation
        translated_text = translate(
            source_lang=source_lang,
            target_lang=target_lang,
            source_text=request.text,
            country=request.country
        )
        
        # Create response
        response = TranslationResponse(
            status="success",
            translated_text=translated_text,
            source_lang=source_lang,
            target_lang=target_lang,
            timestamp=datetime.now(pytz.UTC).strftime('%Y-%m-%d %H:%M:%S'),
            detected_language=source_lang  # Add language detection if available
        )
        
        return response

    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(
            status_code=500,
            detail={
                "error": "Translation error",
                "message": str(e)
            }
        )

@app.get("/languages/")
async def get_languages():
    """
    Get available languages and default settings
    """
    try:
        return JSONResponse(
            content={
                "status": "success",
                "data": {
                    "available_languages": ["English", "Hindi"],
                    "default_source": "English",
                    "default_target": "Hindi",
                    "supported_pairs": [
                        {"source": "English", "target": "Hindi"},
                        {"source": "Hindi", "target": "English"}
                    ]
                },
                "timestamp": datetime.now(pytz.UTC).strftime('%Y-%m-%d %H:%M:%S')
            }
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={
                "error": "Server error",
                "message": str(e)
            }
        )

# Error handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "status": "error",
            "detail": exc.detail,
            "timestamp": datetime.now(pytz.UTC).strftime('%Y-%m-%d %H:%M:%S')
        }
    )

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={
            "status": "error",
            "detail": "Internal server error",
            "message": str(exc),
            "timestamp": datetime.now(pytz.UTC).strftime('%Y-%m-%d %H:%M:%S')
        }
    )

# Health check endpoint
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now(pytz.UTC).strftime('%Y-%m-%d %H:%M:%S'),
        "version": "1.0.0"
    }