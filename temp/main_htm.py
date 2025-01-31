from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from datetime import datetime
import pytz
import os

app = FastAPI(
    title="Voice Recognition Interface",
    description="A web interface for voice recognition and processing",
    version="1.0.0"
)

# Create a directory for static files
static_dir = "static"
os.makedirs(static_dir, exist_ok=True)

# Mount static files and templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

class InferenceRequest(BaseModel):
    query: str
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
            "page_title": "Voice Recognition Interface"
        }
    )

@app.post("/index_voice")
async def run_inference(request: InferenceRequest):
    try:
        # Here you would typically process the voice input
        # For now, we'll just echo back the query
        result = f"Processed query: {request.query}"
        return JSONResponse(
            content={
                "status": "success",
                "data": result,
                "timestamp": datetime.now(pytz.UTC).strftime('%Y-%m-%d %H:%M:%S')
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.now(pytz.UTC).strftime('%Y-%m-%d %H:%M:%S')}