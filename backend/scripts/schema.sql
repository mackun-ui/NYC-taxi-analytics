-- Active: 1771760125516@@pg-2e82378c-alustudent-fab8.g.aivencloud.com@25892@nyc_taxi_analytics
-- Schema generated from backend/scripts/build_db.py
-- and backend/processed_data/cleaned_trips_small.csv

-- Table: zones (renamed from taxi_zones)
-- Derived from backend/processed_data/taxi_zone_lookup.csv
CREATE TABLE IF NOT EXISTS zones (
    "LocationID" INTEGER PRIMARY KEY,
    "Borough" TEXT,
    "Zone" TEXT,
    "service_zone" TEXT
);

-- Table: trips_raw (renamed from trips)
-- Staging table for raw data load
-- Derived from backend/processed_data/cleaned_trips_small.csv
CREATE TABLE IF NOT EXISTS trips_raw (
    "VendorID" BIGINT,
    "tpep_pickup_datetime" TEXT,
    "tpep_dropoff_datetime" TEXT,
    "passenger_count" INTEGER,
    "trip_distance" FLOAT,
    "RatecodeID" INTEGER,
    "store_and_fwd_flag" TEXT,
    "PULocationID" INTEGER,
    "DOLocationID" INTEGER,
    "payment_type" INTEGER,
    "fare_amount" FLOAT,
    "extra" FLOAT,
    "mta_tax" FLOAT,
    "tip_amount" FLOAT,
    "tolls_amount" FLOAT,
    "improvement_surcharge" FLOAT,
    "total_amount" FLOAT,
    "congestion_surcharge" FLOAT,
    "trip_duration_min" FLOAT
);

-- Indexes for trips_raw
CREATE INDEX IF NOT EXISTS idx_fare_amount_raw ON trips_raw ("fare_amount");
CREATE INDEX IF NOT EXISTS idx_PULocationID_raw ON trips_raw ("PULocationID");
CREATE INDEX IF NOT EXISTS idx_DOLocationID_raw ON trips_raw ("DOLocationID");

-- Table: trips (renamed from trips_normalized)
-- Normalized table with Foreign Keys to zones
CREATE TABLE IF NOT EXISTS trips (
    "VendorID" BIGINT,
    "tpep_pickup_datetime" TEXT,
    "tpep_dropoff_datetime" TEXT,
    "passenger_count" INTEGER,
    "trip_distance" FLOAT,
    "RatecodeID" INTEGER,
    "store_and_fwd_flag" TEXT,
    "PULocationID" INTEGER,
    "DOLocationID" INTEGER,
    "payment_type" INTEGER,
    "fare_amount" FLOAT,
    "extra" FLOAT,
    "mta_tax" FLOAT,
    "tip_amount" FLOAT,
    "tolls_amount" FLOAT,
    "improvement_surcharge" FLOAT,
    "total_amount" FLOAT,
    "congestion_surcharge" FLOAT,
    "trip_duration_min" FLOAT,

    CONSTRAINT fk_pickup FOREIGN KEY ("PULocationID") REFERENCES zones("LocationID"),
    CONSTRAINT fk_dropoff FOREIGN KEY ("DOLocationID") REFERENCES zones("LocationID")
);

-- Indexes for trips (normalized)
CREATE INDEX IF NOT EXISTS idx_fare_amount ON trips ("fare_amount");
CREATE INDEX IF NOT EXISTS idx_PULocationID ON trips ("PULocationID");
CREATE INDEX IF NOT EXISTS idx_DOLocationID ON trips ("DOLocationID");
