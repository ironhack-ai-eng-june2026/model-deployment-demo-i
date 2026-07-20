from fastapi import FastAPI

from api.predictor import predict_survival
from api.schemas import PassengerFeatures, PredictionResponse

app = FastAPI(title="Titanic Survival Prediction API")


@app.get("/health")
def health() -> dict:
    """Endpoint to check if the API is available/running"""
    return {"status": "ok"}


@app.post("/predict", response_model=PredictionResponse)
def predict(features: PassengerFeatures) -> PredictionResponse:
    """Predicts survival for a single passenger."""
    return predict_survival(features)
