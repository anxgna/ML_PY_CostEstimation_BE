from sqlalchemy import Column, Integer, Float, Boolean, String, TIMESTAMP, text
from .database import Base

class House(Base):
    __tablename__ = "houses"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    area = Column(Float, nullable=False)
    bedrooms = Column(Integer, nullable=False)
    bathrooms = Column(Integer, nullable=False)
    stories = Column(Integer, nullable=False)
    mainroad = Column(Boolean, nullable=False)
    guestroom = Column(Boolean, nullable=False)
    basement = Column(Boolean, nullable=False)
    hotwaterheating = Column(Boolean, nullable=False)
    airconditioning = Column(Boolean, nullable=False)
    price = Column(Float, nullable=False)
    created_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))

class Prediction(Base):
    __tablename__ = "predictions"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    area = Column(Float, nullable=False)
    bedrooms = Column(Integer, nullable=False)
    bathrooms = Column(Integer, nullable=False)
    stories = Column(Integer, nullable=False)
    mainroad = Column(Boolean, nullable=False)
    guestroom = Column(Boolean, nullable=False)
    basement = Column(Boolean, nullable=False)
    hotwaterheating = Column(Boolean, nullable=False)
    airconditioning = Column(Boolean, nullable=False)
    predicted_price = Column(Float, nullable=False)
    model_version = Column(String(50))
    created_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))

class ModelRegistry(Base):
    __tablename__ = "model_registry"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    version = Column(String(50), unique=True)
    training_date = Column(TIMESTAMP)
    r2_score = Column(Float)
    mse = Column(Float)
    model_path = Column(String(255))
    created_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))
