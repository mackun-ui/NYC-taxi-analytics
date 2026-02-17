import pandas as pd
from datetime import datetime
from .log_utils import log_bad_records

def clean_trip_data(df):
    # cleans the raw yellow taxi data

    initial_count = len(df)

    # remove duplicate rows
    df = df.drop_duplicates()
    print(f"Removed {initial_count - len(df)} duplicate rows")

    # drop rows with missing values
    required_cols = [
        'tpep_pickup_datetime', 'tpep_dropoff_datetime',
        'passenger_count', 'trip_distance', 'fare_amount',
        'PULocationID', 'DOLocationID'
    ]
    missing_mask = df[required_cols].isnull().any(axis=1)
    log_bad_records(df[missing_mask], "missing_values.log")
    df = df[~missing_mask]
    print(f"Dropped {missing_mask.sum()} rowswith missing values")

    # remove impossible trip distances or fare
    invalid_mask = (df['trip_distance'] <= 0) | (df['fare_amount'] <= 0)
    log_bad_records(df[invalid_mask], "invalid_values.log")
    df = df[~invalid_mask]
    print(f"Dropped {invalid_mask.sum()} rows with invalid distance/fare")

    # standardise datetime columns
    df['tpep_pickup_datetime'] = pd.to_datetime(df['tpep_pickup_datetime'], dayfirst=False, errors='coerce')
    df['tpep_dropoff_datetime'] = pd.to_datetime(df['tpep_dropoff_datetime'], dayfirst=False, errors='coerce')

    # compute trip duration in minutes
    df['trip_duration_min'] = (df['tpep_dropoff_datetime'] - df['tpep_pickup_datetime']).dt.total_seconds() / 60
    duration_mask = df['trip_duration_min'] <= 0
    log_bad_records(df[duration_mask], "invalid_duration.log")
    df = df[~duration_mask]
    print(f"Dropped {duration_mask.sum()} row with non-positive durations")
    
    return df

def save_cleaned_data(df, file_path):
    # saves cleaned trip data to CSV for database ingestion
    df.to_csv(file_path, index=False)
    print(f"Saved cleaned data to {file_path}")
