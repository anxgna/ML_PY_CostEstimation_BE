# ML_PY_CostEstimation_BE

## Overview

This is the backend system for the House Price Estimation Platform. It is built using FastAPI and MySQL to predict house prices using a machine learning model, store historical predictions, and provide an interface for managing and retraining models.

## Technology Stack

- **API Framework:** FastAPI
- **Database:** MySQL
- **ORM:** SQLAlchemy
- **Validation:** Pydantic
- **ML Framework:** Scikit-learn
- **Model Serialization:** joblib

## Features

- Accept structured house feature inputs
- Perform ML-based price prediction
- Store prediction history
- API for retraining ML models
- Expose REST APIs for frontend integration
- Persistent storage using MySQL

## Getting Started

### Prerequisites

- Python 3.9+
- MySQL Server
- Environment variables set up

### Installation

1. Clean/Clone the repository:
   ```bash
   git clone https://github.com/your-username/ML_PY_CostEstimation_BE.git
   cd ML_PY_CostEstimation_BE
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Setup environment variables:
   Create a `.env` file in the root directory:
   ```env
   DATABASE_URL=mysql+pymysql://user:password@localhost:3306/housing_db
   ```
   
4. Run the server:
   ```bash
   uvicorn main:app --reload
   ```

## Endpoints

- `GET /health` - Check health status
- `POST /predict` - Get home price prediction
- `GET /predictions` - Retrieve prediction history
- `POST /train` - Trigger ML model retraining
