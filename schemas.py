from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class HouseBase(BaseModel):
    area: float
    bedrooms: int
    bathrooms: int
    stories: int
    mainroad: bool
    guestroom: bool
    basement: bool
    hotwaterheating: bool
    airconditioning: bool

class HouseCreate(HouseBase):
    price: float

class PredictionResponse(HouseBase):
    id: int
    predicted_price: float
    model_version: Optional[str] = None
    created_at: datetime
    
    class Config:
        from_attributes = True
        
class TrainRequest(BaseModel):
    dataset_path: Optional[str] = None
