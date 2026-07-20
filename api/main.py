from fastapi import FastAPI

from api.predictor import predict_survival
from api.schemas import PassengerFeatures, PredictionResponse

from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(title="Titanic Survival Prediction API")


# CORS config (we'll allow requests from any origin)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,  # must be False if allow_origins=["*"]
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health() -> dict:
    """Endpoint to check if the API is available/running"""
    return {"status": "ok"}


@app.post("/predict", response_model=PredictionResponse)
def predict(features: PassengerFeatures) -> PredictionResponse:
    """Predicts survival for a single passenger."""
    return predict_survival(features)
