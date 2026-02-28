import pandas as pd
from sqlalchemy.orm import Session
import database
import models

def seed_database(csv_path="housing.csv"):
    print(f"Loading data from {csv_path}...")
    df = pd.read_csv(csv_path)
    
    # Map 'yes'/'no' strings to boolean True/False
    bool_cols = ["mainroad", "guestroom", "basement", "hotwaterheating", "airconditioning"]
    for col in bool_cols:
        if df[col].dtype == object:
            df[col] = df[col].map({"yes": True, "no": False})
            
    # Connect to the database
    print("Connecting to the database...")
    db: Session = next(database.get_db())
    
    try:
        # Check if data already exists to avoid duplicates
        existing_count = db.query(models.House).count()
        if existing_count > 0:
            print(f"Database already contains {existing_count} records in 'houses' table.")
            choice = input("Do you want to add this data anyway? (y/n): ")
            if choice.lower() != 'y':
                print("Aborting.")
                return

        print("Inserting records into the database...")
        records_to_insert = []
        for _, row in df.iterrows():
            house = models.House(
                area=float(row['area']),
                bedrooms=int(row['bedrooms']),
                bathrooms=int(row['bathrooms']),
                stories=int(row['stories']),
                mainroad=bool(row['mainroad']),
                guestroom=bool(row['guestroom']),
                basement=bool(row['basement']),
                hotwaterheating=bool(row['hotwaterheating']),
                airconditioning=bool(row['airconditioning']),
                price=float(row['price'])
            )
            records_to_insert.append(house)
            
        # Bulk insert for better performance
        db.bulk_save_objects(records_to_insert)
        db.commit()
        print(f"Successfully inserted {len(records_to_insert)} records into the 'houses' table!")
        
    except Exception as e:
        db.rollback()
        print(f"An error occurred: {str(e)}")
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()
