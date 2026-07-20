"""Loads the trained model and wraps prediction logic for the API."""

import os

import joblib
import pandas as pd

from src.data_preprocessing import (
    FEATURES,
    encode_categorical,
    fill_missing_values,
    load_impute_values,
)
from api.schemas import PassengerFeatures

MODEL_PATH = os.path.join(os.path.dirname(__file__), "..", "models", "final_model.pkl")


# Loaded once at import time and reused across requests.
_model = joblib.load(MODEL_PATH)
_impute_values = load_impute_values()


def predict_survival(features: PassengerFeatures) -> dict:
    """Runs the full preprocessing + prediction pipeline for a single passenger."""

    df = pd.DataFrame([features.model_dump()])[FEATURES]

    df = fill_missing_values(df, _impute_values)
    df = encode_categorical(df)

    prediction = _model.predict(df)[0]
    probability = _model.predict_proba(df)[0][1]

    return {
        "survived": int(prediction),
        "survival_probability": float(probability),
    }
