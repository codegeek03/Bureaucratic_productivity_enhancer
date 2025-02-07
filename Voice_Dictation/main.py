from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import speech_recognition as sr
import time
from datetime import datetime
import os
import logging
import threading
from grammar_correction import ProfessionalResponseGenerator    
from grammar_correction import FactChecker    
# [Previous imports and configuration remain the same...]

# Load HTML template from index.html


# [Rest of the FastAPI code remains the same...]

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

HTML_TEMPLATE = ""
try:
    with open("./index.html", "r", encoding='utf-8') as f:
        HTML_TEMPLATE = f.read()
    logger.info("Successfully loaded HTML template")
except Exception as e:
    logger.error(f"Error loading HTML template: {str(e)}")
    raise Exception(f"Failed to load HTML template: {str(e)}")


app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Modify the root endpoint to return the HTML template
@app.get("/", response_class=HTMLResponse)
async def root():
    return HTMLResponse(content=HTML_TEMPLATE)


# Create a directory for storing audio files if it doesn't exist
UPLOAD_DIR = "audio_files"
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

class SpeechRecognizer:
    def __init__(self):
        try:
            self.recognizer = sr.Recognizer()
            self.microphone = sr.Microphone()
            self.is_listening = False
            self.recording_thread = None
            logger.info("Successfully initialized SpeechRecognizer")
        except Exception as e:
            logger.error(f"Error initializing SpeechRecognizer: {str(e)}")
            raise Exception(f"Failed to initialize speech recognition: {str(e)}")
        
    def adjust_for_noise(self):
        try:
            logger.info("Starting noise adjustment")
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=2)
            logger.info("Noise adjustment completed successfully")
            return {"message": "Noise adjustment complete", "status": "success"}
        except Exception as e:
            logger.error(f"Error during noise adjustment: {str(e)}")
            return {"message": f"Error during noise adjustment: {str(e)}", "status": "error"}
    
    def stop_listening(self):
        self.is_listening = False
        logger.info("Stopping recording...")
        if hasattr(self, 'recording_thread') and self.recording_thread:
            self.recording_thread.join()
        return {"success": True, "message": "Recording stopped"}

    def listen(self):
        self.is_listening = True
        try:
            logger.info("Starting audio capture")
            with self.microphone as source:
                logger.info("Listening for audio input...")
                # Reduce timeout and phrase_time_limit for better responsiveness
                audio = self.recognizer.listen(source, timeout=600, phrase_time_limit=40)
                logger.info("Audio captured, processing...")
                
                if not self.is_listening:  # Check if we should stop
                    return {"success": False, "error": "Recording stopped by user"}
                
                try:
                    text = self.recognizer.recognize_google(audio)
                    logger.info("Successfully transcribed audio to text")
                    return {"success": True, "text": text}
                except sr.UnknownValueError:
                    logger.error("Could not understand the audio")
                    return {"success": False, "error": "Could not understand the audio"}
                except sr.RequestError as e:
                    logger.error(f"Could not request results from speech recognition service: {str(e)}")
                    return {"success": False, "error": "Speech recognition service error"}
                    
        except Exception as e:
            logger.error(f"Error during speech recognition: {str(e)}")
            return {"success": False, "error": str(e)}
        finally:
            self.is_listening = False

try:
    speech_engine = SpeechRecognizer()
except Exception as e:
    logger.error(f"Failed to create SpeechRecognizer instance: {str(e)}")
    speech_engine = None

@app.post("/stop-listening")
async def stop_listening():
    if not speech_engine:
        raise HTTPException(status_code=500, detail="Speech recognition not available")
    return speech_engine.stop_listening()

@app.post("/listen")
async def listen_audio():
    if not speech_engine:
        raise HTTPException(status_code=500, detail="Speech recognition not available")
    
    result = speech_engine.listen()
    ans=ProfessionalResponseGenerator().generate_response(result["text"])
    ans = ans["corrected_version"]
    if result["success"]:
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"dictation_{timestamp}.txt"
            filepath = os.path.join(UPLOAD_DIR, filename)
            
            with open(filepath, "w", encoding='utf-8') as f:
                f.write(ans)
            
            logger.info(f"Successfully saved transcription to {filename}")
            return {
                "success": True,
                "text": ans,
                "filename": filename
            }
        except Exception as e:
            logger.error(f"Error saving transcription: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Error saving transcription: {str(e)}")
    else:
        raise HTTPException(status_code=400, detail=result["error"])

# Your other existing endpoints remain the same...

@app.get("/health")
async def health_check():
    """Endpoint to check if the server is running and speech recognition is available"""
    return {
        "status": "healthy",
        "speech_recognition_available": speech_engine is not None,
        "timestamp": datetime.now().isoformat()
    }

@app.post("/adjust-noise")
async def adjust_noise():
    if not speech_engine:
        raise HTTPException(status_code=500, detail="Speech recognition not available")
    
    result = speech_engine.adjust_for_noise()
    if result["status"] == "error":
        raise HTTPException(status_code=500, detail=result["message"])
    return result

@app.post("/listen")
async def listen_audio():
    if not speech_engine:
        raise HTTPException(status_code=500, detail="Speech recognition not available")
    
    result = speech_engine.listen()
    if result["success"]:
        try:
            # Generate filename with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"dictation_{timestamp}.txt"
            filepath = os.path.join(UPLOAD_DIR, filename)
            
            # Save the text to a file
            with open(filepath, "w", encoding='utf-8') as f:
                f.write(result["text"])
            
            logger.info(f"Successfully saved transcription to {filename}")
            return {
                "success": True,
                "text": result["text"],
                "filename": filename
            }
        except Exception as e:
            logger.error(f"Error saving transcription: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Error saving transcription: {str(e)}")
    else:
        raise HTTPException(status_code=400, detail=result["error"])

@app.get("/download/{filename}")
async def download_file(filename: str):
    filepath = os.path.join(UPLOAD_DIR, filename)
    if os.path.exists(filepath):
        return FileResponse(filepath, filename=filename)
    raise HTTPException(status_code=404, detail="File not found")

# Serve the HTML page
@app.get("/", response_class=HTMLResponse)
async def root():
    try:
        with open("./templates/index.html", "r", encoding='utf-8') as f:
            content = f.read()
        return HTMLResponse(content=content)
    except Exception as e:
        logger.error(f"Error serving HTML: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error serving HTML: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=9000)