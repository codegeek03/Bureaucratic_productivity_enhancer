# main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from contentgen import inference

app = FastAPI()

class InferenceRequest(BaseModel):
    query: str

@app.post("/inference")
def run_inference(request: InferenceRequest):
    try:
        result = inference(request.query)
        return {"status": "success", "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
