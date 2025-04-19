import os
import pandas as pd
from datetime import datetime, timedelta
import requests, json
from sqlalchemy.orm import sessionmaker
from models import Earthquake, Base

## Make a class to extract data from api
class E:
    def __init__(self, url: str, params: dict):
        self.url = url
        self.params = params

    def extract(self) -> pd.DataFrame:
        response = requests.get(self.url, params=self.params)
        data = response.json()
        records = []
        for quake in data['features']:
            record = {
                'id': quake['id'],
                'time': quake['properties']['time'],
                'place': quake['properties']['place'],
                'magnitude': quake['properties']['mag'],
                'latitude': quake['geometry']['coordinates'][1],
                'longitude': quake['geometry']['coordinates'][0],
                'depth_km': quake['geometry']['coordinates'][2],
                'details': quake['properties']['detail']
            }
            records.append(record)
            df = pd.DataFrame(records)

        return df
    

## Make a class to transform data
class T:
    def __init__(self, df: pd.DataFrame):
        self.df = df

    def transform(self):
        # Convert time to datetime and format to UTC Yangon time
        self.df['time'] = pd.to_datetime(self.df['time'], unit='ms')
        self.df['time'] = self.df['time'].dt.tz_localize('UTC').dt.tz_convert('Asia/Yangon')
        self.df['time'] = self.df['time'].dt.tz_localize(None)
        self.df['date'] = self.df['time'].dt.date
        self.df['local_time'] = self.df['time'].dt.time.apply(lambda x: x.strftime("%H:%M:%S"))
        self.df['local_time'] = pd.to_datetime(self.df['local_time'], format='%H:%M:%S').dt.time

        # Rearrange columns
        self.df = self.df[['id', 'date', 'local_time', 'place', 'magnitude', 'latitude', 'longitude', 'depth_km', 'details']]
        return self.df


## Make a class to load data to postgres
class L:
    def __init__(self, df: pd.DataFrame, engine):
        self.df = df
        self.engine = engine
        self.Session = sessionmaker(bind=self.engine)

    def load(self):
        with self.Session() as session:
            for _, row in self.df.iterrows():
                quake = Earthquake(
                    id=row['id'],
                    date=row['date'],
                    local_time=row['local_time'],
                    place=row['place'],
                    magnitude=row['magnitude'],
                    latitude=row['latitude'],
                    longitude=row['longitude'],
                    depth_km=row['depth_km'],
                    details=row['details']
                )
                session.merge(quake)
            session.commit()


## Make a class for saving existing data to check for new data
class Saveids:
    def __init__(self, df: pd.DataFrame, file_path: str):
        self.file_path = file_path
        self.df = df

    def save_ids(self):
        with open(self.file_path, 'a') as file:
            for id_ in self.df['id'].unique():
                file.write(f"{id_}\n")

## Make a class for checking new data with saved ids to avoid duplicates
class Loadids:
    def __init__(self, file_path: str):
        self.file_path = file_path

    def load_check_ids(self):
        if os.path.exists(self.file_path):
            with open(self.file_path, 'r') as file:
                save_ids = file.read().splitlines()
        else:
            save_ids = []
        return save_ids
    
