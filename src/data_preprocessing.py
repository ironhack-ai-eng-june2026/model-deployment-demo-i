"""Reusable functions to preprocess the Titanic dataset."""

import json
import os


FEATURES = ["pclass", "sex", "age", "fare", "embarked"]
TARGET = "survived"

SEX_MAPPING = {"male": 0, "female": 1}
EMBARKED_MAPPING = {"S": 0, "C": 1, "Q": 2}

IMPUTE_VALUES_PATH = os.path.join(
    os.path.dirname(__file__), "..", "models", "impute_values.json"
)




def compute_imputation_values(df):
    """
    Computes imputation statistics from the given dataframe.
    - IMPORTANT: must be called on the training split only (never on the full
      dataset or the test split), otherwise the returned statistics leak
      information from the test set into training.

    Returns a dict with:
    - 'age': the median age (robust to outliers).
    - 'embarked': the most frequent embarkation port.
    """

    return {
        "age": df["age"].median(),
        "embarked": df["embarked"].mode()[0],
    }


def save_impute_values(impute_values, path=IMPUTE_VALUES_PATH):
    """
    Persists imputation statistics to a JSON file so they can be reused at
    inference time without recomputing them from the training data.

    Args:
        impute_values: A dict (as returned by `compute_imputation_values`).
        path: Where to write the JSON file. Defaults to `IMPUTE_VALUES_PATH`
            (models/impute_values.json).
    """

    # Cast to native Python types: pandas/numpy scalars (e.g. numpy.float64
    # from `.median()`) aren't JSON-serializable as-is.
    serializable_values = {
        "age": float(impute_values["age"]),
        "embarked": str(impute_values["embarked"]),
    }

    with open(path, "w") as f:
        json.dump(serializable_values, f)


def load_impute_values(path=IMPUTE_VALUES_PATH):
    """
    Loads imputation statistics previously saved by `save_impute_values`.

    Args:
        path: Where to read the JSON file from. Defaults to
            `IMPUTE_VALUES_PATH` (models/impute_values.json).

    Returns:
        A dict with 'age' and 'embarked' fill values, ready to pass to
        `fill_missing_values`.
    """

    with open(path) as f:
        return json.load(f)


def fill_missing_values(df, impute_values):
    """
    Handles missing values in the Titanic dataset by applying imputation.
    - Fills missing 'age' values with the given median age.
    - Fills missing 'embarked' values with the given most frequent category.

    Args:
        df: The dataframe to impute.
        impute_values: A dict (as returned by `compute_imputation_values`)
            with 'age' and 'embarked' fill values. Must be computed from the
            training split and reused as-is for validation/test/inference
            data to avoid data leakage.
    """

    # Create a copy to keep the original dataframe unchanged
    df = df.copy()

    # Replace missing ages with the given median age
    df["age"] = df["age"].fillna(impute_values["age"])

    # Replace missing embarkation ports with the given most common value
    df["embarked"] = df["embarked"].fillna(impute_values["embarked"])

    # Return the dataframe after imputing the missing values
    return df




def encode_categorical(df):
    """
    Converts categorical features into numerical codes:
    - Encodes 'sex' as binary values (male=0, female=1).
    - Encodes 'embarked' as integer labels (S=0, C=1, Q=2).
    """

    # Create a copy to keep the original dataframe unchanged
    df = df.copy()

    # Replace 'sex' categories with their corresponding numeric codes
    df["sex"] = df["sex"].map(SEX_MAPPING)

    # Replace 'embarked' categories with their corresponding numeric codes
    df["embarked"] = df["embarked"].map(EMBARKED_MAPPING)

    # Return the dataframe with the categorical features encoded
    return df
