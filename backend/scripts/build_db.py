import pandas as pd
import psycopg2
from sqlalchemy import create_engine, text
from sqlalchemy.types import Integer, Float, Text, BigInteger
import io
from dotenv import load_dotenv
import os
import sys


script_dir = os.path.dirname(os.path.abspath(__file__))

env_path = os.path.join(script_dir, "../.env")
load_dotenv(env_path)


DATABASE_URL = os.environ.get('DATABASE_URL')

if not DATABASE_URL:
    db_host = os.environ.get('DB_HOST')
    db_port = os.environ.get('DB_PORT', '5432')
    db_user = os.environ.get('DB_USER')
    db_pass = os.environ.get('DB_PASSWORD')
    db_name = os.environ.get('DB_NAME')

    if all([db_host, db_user, db_pass, db_name]):
        # Construct DATABASE_URL from individual components
        # Using URL encoding for password to handle special characters
        from urllib.parse import quote_plus
        DATABASE_URL = f"postgresql://{db_user}:{quote_plus(db_pass)}@{db_host}:{db_port}/{db_name}"
        print("Using database connection parameters from .env")
    else:
        print("Error: DATABASE_URL not found, and connection parameters (DB_HOST, DB_USER, etc.) are incomplete in .env file")
        print(f"Checked path: {os.path.abspath(env_path)}")
        sys.exit(1)



processed_data_dir = os.path.join(script_dir, "../processed_data")
parquet_file = os.path.join(processed_data_dir, "cleaned_trips_small.csv")
zone_csv_path = os.path.join(processed_data_dir, "taxi_zone_lookup.csv")

print(f"Database URL found: {DATABASE_URL.split('@')[1] if '@' in DATABASE_URL else '***'}")


if not os.path.exists(parquet_file):
    print(f"Error: Trip data file not found at {parquet_file}")
    sys.exit(1)

if not os.path.exists(zone_csv_path):
    print(f"Error: Zone lookup file not found at {zone_csv_path}")
    print("Please ensure taxi_zone_lookup.csv is in backend/processed_data/")
    sys.exit(1)

print("Starting optimized database migration to PostgreSQL...")


print(f"Reading trip data from {parquet_file}...")


try:
    df = pd.read_csv(parquet_file)

    if 'tpep_pickup_datetime' in df.columns:
        df['tpep_pickup_datetime'] = df['tpep_pickup_datetime'].astype(str)
    if 'tpep_dropoff_datetime' in df.columns:
        df['tpep_dropoff_datetime'] = df['tpep_dropoff_datetime'].astype(str)

    print(f"Loaded {len(df)} rows.")
except Exception as e:
    print(f"Error reading trip data: {e}")
    sys.exit(1)



dtype_mapping = {
    'VendorID': BigInteger,
    'tpep_pickup_datetime': Text,
    'tpep_dropoff_datetime': Text,
    'passenger_count': Integer,
    'trip_distance': Float,
    'RatecodeID': Integer,
    'store_and_fwd_flag': Text,
    'PULocationID': Integer,
    'DOLocationID': Integer,
    'payment_type': Integer,
    'fare_amount': Float,
    'extra': Float,
    'mta_tax': Float,
    'tip_amount': Float,
    'tolls_amount': Float,
    'improvement_surcharge': Float,
    'total_amount': Float,
    'congestion_surcharge': Float,

    'trip_duration_min': Float,
    'pickup_borough': Text,
    'pickup_zone': Text,
    'dropoff_borough': Text,
    'dropoff_zone': Text,
    'pickup_hour': Integer,
    'day_of_week': Integer
}


dtype_mapping = {k: v for k, v in dtype_mapping.items() if k in df.columns}



try:
    engine = create_engine(DATABASE_URL)
    with engine.connect() as conn:
        # Get current database and schema info
        db_info = conn.execute(text("SELECT current_database(), current_schema()")).fetchone()
        print(f"Connected to: {db_info[0]} (Schema: {db_info[1]})")

        print("Cleaning up existing tables (DRP CASCADE)...")
        conn.execute(text("DROP TABLE IF EXISTS trips CASCADE;"))
        conn.execute(text("DROP TABLE IF EXISTS trips_raw CASCADE;"))
        conn.execute(text("DROP TABLE IF EXISTS zones CASCADE;"))
        conn.commit()
except Exception as e:
    print(f"Error connecting to or cleaning database: {e}")
    print("Please check your database permissions and connection settings.")
    sys.exit(1)


print("Creating 'trips_raw' table schema...")
df.head(0).to_sql("trips_raw", engine, if_exists="replace", index=False, dtype=dtype_mapping)


print("Creating Normalized Tables for ERD...")


try:
    zone_df = pd.read_csv(zone_csv_path)




    if 'LocationID' not in zone_df.columns and zone_df.index.name != 'LocationID':

         pass

    zone_df.to_sql("zones", engine, if_exists="append", index=False, dtype={
        "LocationID": Integer,
        "Borough": Text,
        "Zone": Text,
        "service_zone": Text
    })


    with engine.connect() as con:
        con.execute(text("ALTER TABLE zones ADD PRIMARY KEY (\"LocationID\");"))
        con.commit()
    print("Table 'zones' created and populated.")
except Exception as e:
    print(f"Error processing 'zones': {e}")


print("Creating 'trips' table schema...")
df.head(0).to_sql("trips", engine, if_exists="append", index=False, dtype=dtype_mapping)

print("Creating 'trips_raw' table schema...")
df.head(0).to_sql("trips_raw", engine, if_exists="append", index=False, dtype=dtype_mapping)

with engine.connect() as con:

    try:

        if 'PULocationID' in df.columns and 'DOLocationID' in df.columns:
            con.execute(text("ALTER TABLE trips ADD CONSTRAINT fk_pickup FOREIGN KEY (\"PULocationID\") REFERENCES zones(\"LocationID\");"))
            con.execute(text("ALTER TABLE trips ADD CONSTRAINT fk_dropoff FOREIGN KEY (\"DOLocationID\") REFERENCES zones(\"LocationID\");"))
            con.commit()
            print("Foreign Keys added to 'trips'.")
        else:
            print("Skipping Foreign Keys: PULocationID or DOLocationID missing in trip data.")
    except Exception as e:
        print(f"Error adding FKs to trips_normalized: {e}")



print("Connecting for bulk upload...")
try:

    conn_raw = psycopg2.connect(DATABASE_URL)
    cur = conn_raw.cursor()


    print("Converting dataframe to CSV buffer...")
    csv_buffer = io.StringIO()
    df.to_csv(csv_buffer, index=False, header=False)
    csv_buffer.seek(0)

    print("Copying data to 'trips_raw' table...")
    cur.copy_expert("COPY trips_raw FROM STDIN WITH (FORMAT CSV)", csv_buffer)
    print("Data uploaded to 'trips_raw'.")


    csv_buffer.seek(0)
    print("Copying data to 'trips' table...")
    cur.copy_expert("COPY trips FROM STDIN WITH (FORMAT CSV)", csv_buffer)
    print("Data uploaded to 'trips'.")

    conn_raw.commit()
    print("All data upload complete.")


    print("Creating Indexes...")

    index_cols = ['pickup_borough', 'pickup_hour', 'fare_amount', 'PULocationID', 'DOLocationID']
    for col in index_cols:
        if col in df.columns:
             # Using double quotes for column names due to MixedCase in PostgreSQL
             cur.execute(f'CREATE INDEX IF NOT EXISTS "idx_{col}" ON trips ("{col}");')
             cur.execute(f'CREATE INDEX IF NOT EXISTS "idx_{col}_raw" ON trips_raw ("{col}");')

    conn_raw.commit()
    print("Indexes created.")

    cur.close()
    conn_raw.close()

except Exception as e:
    print(f"Error during bulk upload: {e}")
    if 'conn_raw' in locals():
        conn_raw.rollback()
        conn_raw.close()
    sys.exit(1)

print("Migration completed successfully.")