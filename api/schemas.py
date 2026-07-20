"""Pydantic request/response models for the Titanic prediction API.

Pydantic models describe the shape of the JSON data going in and out of the
API. FastAPI uses them to validate requests, parse JSON into typed Python
objects, and auto-generate the docs at /docs and /redoc.
"""

from typing import Literal, Optional

from pydantic import BaseModel, Field

# `Literal[...]` restricts a field to a fixed set of values (e.g. rejects
# pclass=4 or sex="other") instead of allowing any string or int.


class PassengerFeatures(BaseModel):
    """Request body for POST /predict.
    
    Example of an expected request body:

    {"pclass": 3, "sex": "female", "age": 32, "fare": 7.25, "embarked": "S"}
    """

    # `...` as the first `Field` argument means the field is required.
    pclass: Literal[1, 2, 3] = Field(..., description="Ticket class (1st, 2nd, 3rd).")
    sex: Literal["male", "female"] = Field(..., description="Passenger sex.")

    # `Optional[float]` + `default=None` lets clients omit this field; our
    # pipeline then imputes it (see api/predictor.py).
    age: Optional[float] = Field(
        default=None, description="Passenger age in years. If missing, the training set's median age is used."
    )
    fare: float = Field(..., description="Passenger fare.")

    # Same optional-with-fallback pattern as `age`.
    embarked: Optional[Literal["S", "C", "Q"]] = Field(
        default=None,
        description="Port of embarkation. If missing, the training set's most frequent port is used.",
    )


class PredictionResponse(BaseModel):
    """
    Response body returned by POST /predict.
    
    Example of a response body:

    {"survived": 1, "survival_probability": 0.82}

    Used as the endpoint's `response_model`, which validates the outgoing
    data and documents the response shape in the interactive docs.
    """

    survived: int = Field(..., description="Predicted survival: 0 (did not survive) or 1 (survived).")
    survival_probability: float = Field(..., description="Predicted probability of survival.")
