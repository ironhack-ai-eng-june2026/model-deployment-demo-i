# Machine Learning - Model Deployment Demo

This repo contains the boilerplate code to be used for a demo on model deployment, using the classic [Titanic dataset](https://www.kaggle.com/c/titanic) (loaded via `seaborn`) to predict passenger survival.

The demo includes a very basic EDA and intentionally skips advanced preprocessing, feature engineering, hyperparameter tuning, and cross-validation to keep the focus on project structure.

The demo includes a very basic EDA and intentionally skips advanced preprocessing, feature engineering, hyperparameter tuning, and model validation (using a train/validation/test split or cross-validation) to keep the focus on project structure.

The goal is to demonstrate code organization and common patterns, not to build a perfect model.


## How to run

a) **On macOS/Linux**

```shell
# Create a virtual environment
python3 -m venv .venv

# Activate the virtual environment
source .venv/bin/activate

# Install the project dependencies
pip install -r requirements.txt

# Run the FastAPI application
uvicorn api.main:app --reload
```


b) **On Windows**

```shell
# Create a virtual environment
python -m venv .venv

# Activate the virtual environment
.\.venv\Scripts\activate

# Install the project dependencies
pip install -r requirements.txt

# Run the FastAPI application
uvicorn api.main:app --reload
```


## API documentation

See: http://localhost:8000/docs


