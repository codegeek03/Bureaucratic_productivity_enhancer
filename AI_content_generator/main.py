from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from contentgen import inference
from datetime import datetime
import pytz

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

class InferenceRequest(BaseModel):
    query: str

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    current_time = datetime.now(pytz.UTC).strftime('%Y-%m-%d %H:%M:%S')
    return templates.TemplateResponse(
        "inference.html", 
        {"request": request, "current_time": current_time, "user": "SRINJOY59"}
    )

@app.post("/inference")
def run_inference(request: InferenceRequest):
    try:
        result = inference(request.query)
        return {"status": "success", "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))