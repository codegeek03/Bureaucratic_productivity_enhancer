from fastapi import FastAPI, HTTPException, Request, File, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from datetime import datetime
import pytz
from generation import ImageAnalyzer
import shutil
import os
import uvicorn
from pathlib import Path
from uuid import uuid4

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    current_time = datetime.now(pytz.UTC).strftime('%Y-%m-%d %H:%M:%S')
    return templates.TemplateResponse(
        "analyze.html",
        {"request": request, "current_time": current_time, "user": "SRINJOY59"}
    )

@app.post("/analyze")
async def analyze_image(file: UploadFile = File(...)):
    try:
        if not file.content_type.startswith('image/'):
            raise HTTPException(
                status_code=400,
                detail="File must be an image"
            )
        
        file_extension = file.filename.split('.')[-1]
        unique_filename = f"{uuid4()}.{file_extension}"
        file_path = UPLOAD_DIR / unique_filename
        
        with file_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        analyzer = ImageAnalyzer(str(file_path))
        result = analyzer.analyze_image()
        
        os.remove(file_path)
        
        return {
            "status": "success",
            "filename": file.filename,
            "data": result
        }
        
    except Exception as e:
        if 'file_path' in locals() and file_path.exists():
            os.remove(file_path)
        raise HTTPException(status_code=500, detail=str(e))
    
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=7860, reload=True)