from fastapi import FastAPI
from pydantic import BaseModel
from joblib import load
import os

# Service sederhana untuk inferensi sentimen
# Jalankan: uvicorn src.app:app --host 0.0.0.0 --port 8000

MODEL_PATH = os.getenv("MODEL_PATH", "models/model.pkl")

app = FastAPI(title="Sentiment Analysis API", version="1.0.0")

class PredictRequest(BaseModel):
    text: str

class PredictResponse(BaseModel):
    label: str
    probability: float

# Lazy load model saat startup
model = None

@app.on_event("startup")
def load_model():
    global model
    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError(
            f"Model not found at {MODEL_PATH}. Jalankan pipeline DVC terlebih dahulu (dvc repro)."
        )
    model = load(MODEL_PATH)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/predict", response_model=PredictResponse)
def predict(req: PredictRequest):
    text = req.text.strip()
    if not text:
        return {"label": "unknown", "probability": 0.0}
    # Pipeline sklearn: .predict_proba mengembalikan probabilitas kelas [0, 1]
    proba = model.predict_proba([text])[0]
    p_neg, p_pos = float(proba[0]), float(proba[1])
    label = "positive" if p_pos >= p_neg else "negative"
    prob = max(p_pos, p_neg)
    return {"label": label, "probability": prob}
