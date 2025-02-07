from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from speech_Recog import SpeechToText
from grammar_correction import ProfessionalResponseGenerator
import shutil
import os
from typing import Optional
from pydantic import BaseModel

app = FastAPI(
    title="Speech Processing and Grammar Correction API",
    description="API for speech-to-text conversion and grammar correction",
    version="1.0.0"
)

UPLOAD_DIR = "temp_uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

class TranscriptionResponse(BaseModel):
    transcription: str
    corrected_response: str

@app.post("/process-audio/", response_model=TranscriptionResponse)
async def process_audio(
    file: UploadFile = File(...),
    model_name: Optional[str] = "mixtral-8x7b-32768"
):
    """
    Process audio file and return both transcription and grammar-corrected response.
    
    Args:
        file: Audio file to process
        model_name: Optional model name for the grammar correction (default: mixtral-8x7b-32768)
    """
    try:
        # Save the uploaded file temporarily
        temp_file_path = os.path.join(UPLOAD_DIR, file.filename)
        with open(temp_file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Initialize speech recognition
        speech_recognizer = SpeechToText()
        
        # Perform transcription
        transcribed_text = speech_recognizer.transcribe(temp_file_path)
        
        # Initialize grammar correction
        generator = ProfessionalResponseGenerator(model_name=model_name)
        
        # Generate corrected response
        corrected_response = generator.generate_response(transcribed_text)
        
        # Clean up the temporary file
        os.remove(temp_file_path)
        
        return TranscriptionResponse(
            transcription=transcribed_text,
            corrected_response=corrected_response
        )
        
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": f"An error occurred: {str(e)}"}
        )

@app.post("/correct-text/")
async def correct_text(text: str, model_name: Optional[str] = "mixtral-8x7b-32768"):
    """
    Process text input and return grammar-corrected response.
    
    Args:
        text: Input text to process
        model_name: Optional model name for the grammar correction
    """
    try:
        generator = ProfessionalResponseGenerator(model_name=model_name)
        corrected_response = generator.generate_response(text)
        
        return {"corrected_response": corrected_response}
        
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": f"An error occurred: {str(e)}"}
        )

@app.get("/")
async def root():
    """Root endpoint returning API information"""
    return {
        "message": "Speech Processing and Grammar Correction API",
        "version": "1.0.0",
        "endpoints": [
            "/process-audio/ - POST endpoint for audio processing",
            "/correct-text/ - POST endpoint for text correction"
        ]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=9000)