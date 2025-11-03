# backend/app.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import uvicorn
import os
from model_utils import load_model

# ---- CONFIG ----
MODEL_PATH = "model.joblib"



app = FastAPI(title="Student Performance Predictor")

# ---- CORS ----
app.add_middleware(
    CORSMiddleware,
    allow_origin_regex=".*",     # allow *any* origin (temporary for testing)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---- Mount Frontend Build ----
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def root():
    return {"message": "Backend is running. Go to /docs for API documentation."}


# ---- MODELS ----
class PredictRequest(BaseModel):
    weekly_self_study_hours: float = Field(..., example=5.0)
    attendance_percentage: float = Field(..., example=85.0)
    class_participation: float = Field(..., example=4.0)
    total_score: float = Field(..., example=67.5)

class PredictResponse(BaseModel):
    prediction: str
    probability: float

# ---- LOAD MODEL ----
model = None

@app.on_event("startup")
def load_model_on_startup():
    global model
    print("🔄 Loading model...")
    model = load_model(MODEL_PATH)
    if model is not None:
        print("✅ Model loaded successfully!")
    else:
        print("❌ Failed to load model!")


# ---- HEALTH ----
@app.get("/health")
def health():
    return {"status": "ok"}

# ---- PREDICT ----
@app.post("/predict", response_model=PredictResponse)
def predict(req: PredictRequest):
    global model
    print("📩 Incoming prediction request:", req.dict())

    if model is None:
        raise HTTPException(status_code=500, detail="Model not loaded")

    try:
        X = [[
            req.weekly_self_study_hours,
            req.attendance_percentage,
            req.class_participation,
            req.total_score
        ]]
        prob = model.predict_proba(X)[0][1]
        pred = model.predict(X)[0]
        print(f"✅ Prediction done: {pred}, probability: {prob}")
        return PredictResponse(prediction="pass" if int(pred) == 1 else "fail", probability=float(prob))
    except Exception as e:
        print("❌ Prediction error:", e)
        raise HTTPException(status_code=500, detail=str(e))


# ---- MAIN ----
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("app:app", host="0.0.0.0", port=port)
