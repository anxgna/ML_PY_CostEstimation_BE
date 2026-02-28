# Render.com Deployment Walkthrough

Render is an excellent platform for hosting FastAPI backends, especially for Machine Learning apps, as it avoids the strict size limitations present in serverless platforms like Vercel.

Since you've already successfully migrated your database to **Supabase (PostgreSQL)**, you only need to deploy your Python backend!

## Step 1: Push Your Code to GitHub

Render deploys directly from your GitHub repository.

1. Open a terminal in your project directory.
2. If you haven't already initialized Git, run:
```bash
git init
git add .
git commit -m "Initial commit for Render deployment"
```
3. Create a new repository on GitHub and follow their instructions to push your local code to the `main` branch.

## Step 2: Create the Render Web Service (FastAPI)

1. Create an account on [Render.com](https://render.com/).
2. On the Render Dashboard, click **New** -> **Web Service**.
3. Select **"Build and deploy from a Git repository"** and connect your GitHub account. Select your newly created repository.
4. Configure the Web Service:
   * **Name**: `house-price-api` (or any name you prefer)
   * **Region**: Choose the one closest to you.
   * **Runtime**: `Python 3`
   * **Build Command**: `pip install -r requirements.txt`
   * **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
5. Click **Advanced** to add an **Environment Variable**:
   * **Key**: `DATABASE_URL`
   * **Value**: *(Paste your Supabase connection string starting with `postgresql://` here)*
6. Click **Create Web Service**.

## Step 3: Monitor Deployment and Test

Render will automatically pull your code from GitHub, install the requirements (`fastapi`, `scikit-learn`, `psycopg2-binary`, etc.), and run the start command.

1. Watch the **Logs** tab in Render to ensure there are no build errors.
2. Once the deploy says **"Live"**, Render will give you a public URL (e.g., `https://house-price-api-XXXX.onrender.com`).
3. Append `/docs` to that URL (e.g., `https://house-price-api-XXXX.onrender.com/docs`) to view your live, interactive API documentation on the internet! 

## Step 4 (Optional): Update the Frontend

Once your backend API is live on Render:
1. Open your local `app.py` (the Gradio interface).
2. Change the `API_URL` to point to your new Render endpoint:
   ```python
   API_URL = "https://house-price-api-XXXX.onrender.com/predict"
   ```
3. You can now host the frontend anywhere (like HuggingFace Spaces or another Web Service on Render), and it will talk to your Render backend and Supabase database perfectly!
