from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from . import models, schemas, database, ml_pipeline

# Create tables
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="House Price Estimation API")

# Mock loaded model
active_model = None
active_model_version = "v1.0"

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
    # Mock training
    return {"message": "Model trained successfully", "r2_score": 0.85, "mse": 12000000}
