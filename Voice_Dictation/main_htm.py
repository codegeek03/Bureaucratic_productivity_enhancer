from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from datetime import datetime
import pytz
import os

app = FastAPI(
    title="Voice Dictation Interface",
    description="A web interface for voice dictation and text download",
    version="1.0.0"
)

# Create directories for static files and transcripts
static_dir = "static"
transcripts_dir = "transcripts"
os.makedirs(static_dir, exist_ok=True)
os.makedirs(transcripts_dir, exist_ok=True)

# Mount static files and templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

class TranscriptRequest(BaseModel):
    text: str
    user_id: str = "codegeek03"

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    current_time = datetime.now(pytz.UTC).strftime('%Y-%m-%d %H:%M:%S')
    return templates.TemplateResponse(
        "index_voice.html", 
        {
            "request": request, 
            "current_time": current_time, 
            "user": "codegeek03",
            "page_title": "Voice Dictation Interface"
        }
    )

@app.post("/save_transcript")
async def save_transcript(request: TranscriptRequest):
    try:
        filename = f"transcript_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{request.user_id}.txt"
        filepath = os.path.join(transcripts_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(request.text)
            
        return JSONResponse(
            content={
                "status": "success",
                "filename": filename,
                "message": "Transcript saved successfully"
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/download/{filename}")
async def download_transcript(filename: str):
    filepath = os.path.join(transcripts_dir, filename)
    if os.path.exists(filepath):
        return FileResponse(
            filepath,
            media_type="text/plain",
            filename=filename
        )
    raise HTTPException(status_code=404, detail="File not found")

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now(pytz.UTC).strftime('%Y-%m-%d %H:%M:%S')
    }