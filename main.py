import psycopg2
from datetime import datetime
from etl_utils import E, T, L, Saveids, Loadids
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker, declarative_base
from models import Base, Earthquake
import logging

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

url = "https://earthquake.usgs.gov/fdsnws/event/1/query"
params = {
        "format":"geojson",
        "latitude":22.697,
        "longitude":96.069,
        "maxradiuskm": 600,
        "starttime": "2025-02-01",
        "endtime": datetime.now().strftime("%Y-%m-%d")
    }

## Call functions to extract, transform, and load
try:
    logging.info("Starting ETL process...")
    logging.info("Extracting data from API...")
    etl = E(url, params) # Assign the extract class to a variable
    raw_df = etl.extract() # Call the extract method to get the data
except Exception as e:
    logging.error(f"Error extracting data: {e}")
    exit(1) # Abnormal exit

## Use try except finally to check for new data. If there is no new data, it will not save the ids to txt file.
load = Loadids('ids.txt')
ex_ids = load.load_check_ids()
raw_df = raw_df[~raw_df['id'].isin(ex_ids)]

## If no new data, exit the program
if raw_df.empty:
    logging.info(f"No new data found!")
    exit(0) # Normal exit cause no new data

save  = Saveids(raw_df, 'ids.txt')
save.save_ids()
logging.info(f"New earthquake found!")
print("Data Updating...")

## Transform the data
logging.info("Transforming data...")
transformed_df = T(raw_df).transform()
print(transformed_df.head())
print(transformed_df.info())

## Load the data to PostgreSQL
postgres_url = 'postgresql://neondb_owner:npg_hvASCWw4xkT1@ep-solitary-water-a1eo9cj6-pooler.ap-southeast-1.aws.neon.tech/neondb?sslmode=require'
engine = create_engine(postgres_url)
Session = sessionmaker(bind=engine)
session = Session()

## Create the table if doesn't exist
inspector = inspect(engine)
if not inspector.has_table(Earthquake.__tablename__):
    Base.metadata.create_all(engine)
    logging.info(f"Table {Earthquake.__tablename__} created!")

load_to_db = L(transformed_df, engine)
try:
    logging.info("Loading data to PostgreSQL...")
    load_to_db.load()
    logging.info("Data loaded successfully!")
except Exception as e:
    logging.error(f"Error loading data to PostgreSQL: {e}")
    exit(1)
finally:
    session.close()
    engine.dispose()





     


    



