import joblib
from sklearn.linear_model import LinearRegression
import numpy as np
import os

MODEL_DIR = "models"
os.makedirs(MODEL_DIR, exist_ok=True)

# Stub ML Pipeline
def train_model(X, y):
    model = LinearRegression()
    model.fit(X, y)
    
    # Mock scores
    r2_score = 0.85
    mse_score = 12000000.0
    
    model_path = os.path.join(MODEL_DIR, "active_model.joblib")
    joblib.dump(model, model_path)
    
    return model, r2_score, mse_score, model_path

def predict_price(model, features):
    if not model:
        # Mock prediction if model not loaded
        return sum(features) * 1000
    return model.predict([features])[0]
