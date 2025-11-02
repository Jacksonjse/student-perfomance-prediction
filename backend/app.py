# backend/app.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Optional
import uvicorn
from model_utils import load_model, NUMERIC_FEATURES
from fastapi.middleware.cors import CORSMiddleware

MODEL_PATH = "model.joblib"

app = FastAPI(title="Student Pass/Fail Predictor")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # set to your frontend origin in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class PredictRequest(BaseModel):
    weekly_self_study_hours: float = Field(..., example=5.0)
    attendance_percentage: float = Field(..., example=85.0)
    class_participation: float = Field(..., example=4.0)
    total_score: float = Field(..., example=67.5)

class PredictResponse(BaseModel):
    prediction: str
    probability: float

model = None

@app.on_event("startup")
def load_model_on_startup():
    global model
    model = load_model(MODEL_PATH)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/predict", response_model=PredictResponse)
def predict(req: PredictRequest):
    global model
    if model is None:
        raise HTTPException(status_code=500, detail="Model not loaded")
    X = [[
        req.weekly_self_study_hours,
        req.attendance_percentage,
        req.class_participation,
        req.total_score
    ]]
    prob = model.predict_proba(X)[0][1]  # probability of '1' (pass)
    pred = model.predict(X)[0]
    return PredictResponse(prediction="pass" if int(pred)==1 else "fail", probability=float(prob))

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
