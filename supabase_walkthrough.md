# Supabase Database Migration Guide

Supabase is a fantastic free-tier cloud database provider, but it uses **PostgreSQL**, not MySQL. 

Because our backend uses `SQLAlchemy` (an Object-Relational Mapper), switching from MySQL to PostgreSQL is incredibly easy. We only need to change a few lines of code and install the correct PostgreSQL driver.

Follow these explicit steps to move your local MySQL database into the Supabase cloud.

---

## Step 1: Create a Supabase Database

1. Go to [Supabase.com](https://supabase.com/).
2. Click **Start your project** (Sign up with GitHub if asked).
3. Click **New Project** and select your organization.
4. Fill in the details:
   - **Name**: `House Price DB`
   - **Database Password**: Generate a secure password and **SAVE IT SOMEWHERE SAFE**. You will need this later.
   - **Region**: Choose the region closest to you.
5. Click **Create new project**. 
*(Wait ~1-2 minutes for the database to provision).*

---

## Step 2: Get your Connection String

1. Once the dashboard loads, navigate to the **Settings** (gear icon) on the bottom left.
2. Select **Database** under the Configuration list.
3. Scroll down until you see the **Connection String** section.
4. Select the **URI** tab. It will look like this:
   `postgresql://postgres.xxxxxxxxxxxx:[YOUR-PASSWORD]@aws-0-us-east-1.pooler.supabase.com:6543/postgres`
5. Copy this URL. Replace `[YOUR-PASSWORD]` with the secure password you generated in Step 1.

---

## Step 3: Update your Backend Code

We must instruct Python to use PostgreSQL instead of MySQL.

### 1. Install the PostgreSQL Driver
Open your terminal (ensure your `venv` is active) and install `psycopg2`, the adapter for Python and PostgreSQL:

```bash
pip install psycopg2-binary
```

### 2. Update `requirements.txt`
In `/home/anugna/Documents/projects/ML_PY_CostEstimation_BE/requirements.txt`:
* **Remove**: `pymysql>=1.1.0`
* **Add**: `psycopg2-binary>=2.9.9`

### 3. Update your `.env` File
In `/home/anugna/Documents/projects/ML_PY_CostEstimation_BE/.env`:
* Delete your old `mysql+pymysql://` string.
* Add your new Supabase connection string. 
* **CRITICAL**: SQLAlchemy requires the connection protocol to be `postgresql://` instead of `postgres://`. Ensure your variable starts correctly:

```env
DATABASE_URL=postgresql://postgres.xxxxxxxxxxxx:YOUR_PASSWORD_HERE@aws-0-us-east-1.pooler.supabase.com:6543/postgres
```

---

## Step 4: Provision the Cloud Tables

Because SQLAlchemy automatically creates missing tables based on your `models.py` file, all you have to do is restart your FastAPI server!

1. Stop your currently running FastAPI server (`Ctrl+C`).
2. Start it again:
   ```bash
   uvicorn main:app --reload
   ```
3. Watch your terminal logs. Because `models.Base.metadata.create_all` triggers on startup, SQLAlchemy will automatically reach out to Supabase and create your `houses`, `predictions`, and `model_registry` tables.

Check your Supabase dashboard -> **Table Editor** on the left menu. You should see your new, empty tables!

---

## Step 5: Seed the New Cloud Database

Currently, your Supabase cloud DB is empty. Let's push your `housing.csv` dataset into the cloud so your model can train against it if deployed later.

Run the seeder script we built earlier:
```bash
python seed_db.py
```

It will connect to the cloud DB (via the `.env` variable) and insert all 545 records.

> ✅ **You are done!** Your entire project is now running locally on your laptop, but saving and reading data directly from the Supabase cloud!
