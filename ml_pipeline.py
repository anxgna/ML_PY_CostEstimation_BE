import os
import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score, mean_squared_error
import joblib
from datetime import datetime

MODEL_DIR = "models"
os.makedirs(MODEL_DIR, exist_ok=True)

def load_dataset(csv_path: str):
    df = pd.read_csv(csv_path)
    bool_cols = ["mainroad", "guestroom", "basement", "hotwaterheating", "airconditioning"]
    for col in bool_cols:
        if df[col].dtype == object:
            df[col] = df[col].map({"yes": 1.0, "no": 0.0})
            
    feature_cols = ["area", "bedrooms", "bathrooms", "stories", "mainroad", "guestroom",
                    "basement", "hotwaterheating", "airconditioning"]
    X = df[feature_cols]
    y = df["price"]
    return X, y

# Train model from CSV and save
def train_model_from_csv(csv_path: str):
    X, y = load_dataset(csv_path)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Define the parameter grid for Random Forest
    param_grid = {
        'n_estimators': [50, 100, 200],
        'max_depth': [None, 10, 20],
        'min_samples_split': [2, 5]
    }
    
    # Initialize the model and perform Grid Search Cross Validation
    rf = RandomForestRegressor(random_state=42)
    grid_search = GridSearchCV(estimator=rf, param_grid=param_grid, cv=5, n_jobs=-1, scoring='r2')
    grid_search.fit(X_train, y_train)
    
    # The best model found by GridSearchCV
    model = grid_search.best_estimator_
    
    # Evaluate
    y_pred = model.predict(X_test)
    r2 = r2_score(y_test, y_pred)
    mse = mean_squared_error(y_test, y_pred)
    # Save model
    version = datetime.utcnow().strftime("%Y%m%d%H%M%S")
    model_path = os.path.join(MODEL_DIR, f"model_{version}.joblib")
    joblib.dump(model, model_path)
    return model, r2, mse, version, model_path

# Simple prediction wrapper used by API
def predict_price(model, features):
    if model is None:
        # Return a mock value if model not loaded
        return sum(features) * 1000
    
    # Create a DataFrame to preserve feature names and avoid scikit-learn warnings
    feature_cols = ["area", "bedrooms", "bathrooms", "stories", "mainroad", "guestroom",
                    "basement", "hotwaterheating", "airconditioning"]
    import pandas as pd
    features_df = pd.DataFrame([features], columns=feature_cols)
    return model.predict(features_df)[0]

if __name__ == "__main__":
    print("Training model... (This might take a few moments due to hyperparameter tuning)")
    model, r2, mse, version, path = train_model_from_csv("housing.csv")
    print(f"Model {version} trained successfully using Random Forest!")
    print(f"Best Parameters: {model.get_params()}")
    print(f"R2 Score: {r2:.4f}, MSE: {mse:.4f}")
    print(f"Saved to {path}")
