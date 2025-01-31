from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

# Import your existing translation functions
from translator import translate  # assuming your file is named translator.py

app = FastAPI(
    title="Translation API",
    description="API for translating text between different languages",
    version="1.0.0"
)

# Create a Pydantic model for the request body
class TranslationRequest(BaseModel):
    source_lang: str
    target_lang: str
    source_text: str
    country: Optional[str] = ""
    max_tokens: Optional[int] = 1000

# Create a Pydantic model for the response
class TranslationResponse(BaseModel):
    translated_text: str
    source_lang: str
    target_lang: str

@app.post("/translate", response_model=TranslationResponse)
async def translate_text(request: TranslationRequest):
    """
    Translate text from source language to target language
    
    Args:
        request: TranslationRequest object containing:
            - source_lang: Source language code
            - target_lang: Target language code
            - source_text: Text to translate
            - country: Optional country for regional language variants
            - max_tokens: Optional maximum tokens per chunk
    
    Returns:
        TranslationResponse object containing the translated text and language information
    """
    try:
        translated_text = translate(
            source_lang=request.source_lang,
            target_lang=request.target_lang,
            source_text=request.source_text,
            country=request.country,
            max_tokens=request.max_tokens
        )
        
        return TranslationResponse(
            translated_text=translated_text,
            source_lang=request.source_lang,
            target_lang=request.target_lang
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Add a health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=9000)
