# This file loads: parquet trip data, zone lookup CSV, and geojson zones

import pandas as pd
import json
import os

def load_trip_data(file_path):
    # loads the yellow taxi trip data from a .parquet file
    file_path = file_path.lower()

    if file_path.endswith(".csv"):
        df = pd.read_csv(file_path)
    elif file_path.endswith(".parquet"):
        df = pd.read_parquet(file_path)
    else:
        raise ValueError(f"Unsupported file type: {file_path}")

    
    if file_path.endswith(".parquet"):
        df = pd.read_parquet(file_path)
    else: 
        df = pd.read_csv(file_path)

    print(f"Loaded trip data with {len(df)} rows and {len(df.columns)} columns.")
    return df

def load_zone_lookup(file_path):
    # loads the taxi zone lookup CSV mapping LocationID to Borough and Zone
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"{file_path} does not exist")
    
    df = pd.read_csv(file_path)
    print(f"Loaded zone lookup: {len(df)} rows, {len(df.columns)} columns.")
    return df

def load_geojson(file_path):
    # loads taxi_zones.geojson spatial metadata
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"{file_path} does not exist")
    
    with open(file_path, "r") as f:
        geojson_data = json.load(f)
    
    print(f"Loaded GeoJSON with {len(geojson_data['features'])} features")
    return geojson_data