from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

import models
import schemas
import database
import ml_pipeline

# Create tables
models.Base.metadata.create_all(bind=database.engine)

description = """
House Price Estimation API helps you estimate house prices based on various features.

## Features
* **Predict Price:** Submit house features to get an estimated price.
* **Get Predictions:** Retrieve history of previous predictions.
* **Train Model:** Trigger model training on the dataset.
"""

app = FastAPI(
    title="House Price Estimation API",
    description=description,
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)
@app.get("/")
def home():
    return {"message": "House Price Estimation API is running 🚀"}

from fastapi.responses import Response

@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return Response(content=b"", media_type="image/x-icon")

import os
import glob
import joblib

# Load the latest model dynamically
def load_latest_model():
    if not os.path.exists("models"):
        return None, "v1.0"
    model_files = glob.glob(os.path.join("models", "*.joblib"))
    if not model_files:
        return None, "v1.0"
    latest_model_file = max(model_files, key=os.path.getctime)
    model = joblib.load(latest_model_file)
    version = os.path.basename(latest_model_file).replace("model_", "").replace(".joblib", "")
    return model, version

active_model, active_model_version = load_latest_model()

@app.get("/health")
def health_check():
    return {
        "status": "up",
        "api": "FastAPI",
        "model_loaded": active_model is not None,
        "database": "Mysql (configured)"
    }

@app.post("/predict", response_model=schemas.PredictionResponse)
def predict_price(request: schemas.HouseBase, db: Session = Depends(database.get_db)):
    features = [
        request.area, request.bedrooms, request.bathrooms, request.stories,
        float(request.mainroad), float(request.guestroom), float(request.basement),
        float(request.hotwaterheating), float(request.airconditioning)
    ]
    
    predicted_price = ml_pipeline.predict_price(active_model, features)
    
    db_prediction = models.Prediction(
        **request.model_dump(),
        predicted_price=predicted_price,
        model_version=active_model_version
    )
    db.add(db_prediction)
    db.commit()
    db.refresh(db_prediction)
    return db_prediction

@app.get("/predictions", response_model=List[schemas.PredictionResponse])
def get_predictions(skip: int = 0, limit: int = 100, db: Session = Depends(database.get_db)):
    predictions = db.query(models.Prediction).offset(skip).limit(limit).all()
    return predictions

@app.post("/train")
def train_model(req: schemas.TrainRequest, db: Session = Depends(database.get_db)):
    global active_model
    global active_model_version

    dataset_path = req.dataset_path or "housing.csv"
    if not os.path.exists(dataset_path):
        raise HTTPException(status_code=400, detail="Dataset not found")
        
    model, r2, mse, version, model_path = ml_pipeline.train_model_from_csv(dataset_path)
    
    # Reload model hot
    active_model = model
    active_model_version = version

    # Save to registry
    registry_entry = models.ModelRegistry(
        version=version,
        r2_score=r2,
        mse=mse,
        model_path=model_path
    )
    db.add(registry_entry)
    db.commit()

    return {"message": "Model trained successfully", "version": version, "r2_score": r2, "mse": mse}
