# Local Setup Guide for ML_PY_CostEstimation_BE

Follow these steps to get the house price estimation backend running on your local machine.

## Prerequisites
1. **Python 3.9+**
2. **MySQL Server** installed and running on your machine.

---

## Step 1: Set up MySQL Database

You need to create the database that the application will use.
Log in to your MySQL shell:
```bash
mysql -u root -p
```

Create the database:
```sql
CREATE DATABASE housing_db;
```
*(Optional)* Create a user specifically for this app with a password (replace `password`):
```sql
CREATE USER 'user'@'localhost' IDENTIFIED BY 'password';
GRANT ALL PRIVILEGES ON housing_db.* TO 'user'@'localhost';
FLUSH PRIVILEGES;
```

---

## Step 2: Set up a Python Virtual Environment

Navigate to the project directory:
```bash
cd /home/anugna/Documents/projects/ML_PY_CostEstimation_BE
```

Create a virtual environment (this keeps dependencies isolated):
```bash
python3 -m venv venv
```
---

## Step 3: Install Dependencies

With your virtual environment activated, install the required packages:
```bash
pip install -r requirements.txt
```

---

## Step 4: Configure Environment Variables

Create a file named `.env` in the root of the project folder:
```bash
touch .env
```

Add your database connection string to the `.env` file. Open the file in an editor and add:
```env
DATABASE_URL=mysql+pymysql://user:password@localhost:3306/housing_db
```
*(Make sure to replace `user` and `password` with your actual MySQL credentials from Step 1).*

---

## Step 5: Run the FastAPI Server

Start the FastAPI application using Uvicorn:
```bash
uvicorn main:app --reload
```

---

## Step 6: Test the API

The server will start at `http://127.0.0.1:8000`. 
FastAPI automatically generates an interactive API documentation page!

1. Open a browser and go to: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
2. You will see the Swagger UI where you can test all endpoints:
   - **`GET /health`**: Returns system health.
   - **`POST /predict`**: Submit house parameters (like area, bedrooms) to get a mock predicted price.
   - **`GET /predictions`**: View history of predictions.
   - **`POST /train`**: Trigger training (stubbed for now).

When you first start the app, SQLAlchemy will automatically create all necessary tables (`houses`, `predictions`, `model_registry`) in your MySQL database based on the file `models.py`.
