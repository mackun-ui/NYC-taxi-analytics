# NYC Taxi Analytics App

## Overview

This project is an enterprise-level fullstack analytics system built
using official New York City Taxi & Limousine Commission (TLC) datasets.
It implements a complete data engineering and application development
lifecycle:

-   Raw data ingestion (.parquet, .csv, .geojson)
-   Data cleaning and preprocessing
-   Feature engineering
-   Normalized relational database implementation
-   RESTful backend API development
-   Interactive frontend dashboard

The system transforms raw taxi trip records into structured, queryable,
and analytically meaningful insights for urban mobility analysis.

------------------------------------------------------------------------

## Learning Objectives Demonstrated

This project fulfills the following technical competencies:

-   Real-world data preprocessing and anomaly handling
-   Relational schema normalization and indexing
-   Backend API development (Flask)
-   Fullstack system integration
-   Analytical feature engineering
-   Interactive data visualization
-   End-to-end system design and implementation

------------------------------------------------------------------------

## Dataset Components

The system integrates three official NYC TLC data components:

1.  yellow_tripdata (Fact Table)
    -   Trip timestamps
    -   Distances
    -   Fare breakdowns
    -   Location IDs
    -   Payment metadata
2.  taxi_zone_lookup (Dimension Table)
    -   LocationID to Borough/Zone mappings
3.  taxi_zones (GeoJSON Spatial Metadata)
    -   Polygon boundaries for taxi zones

These datasets were programmatically integrated to create a relational
analytical environment.

------------------------------------------------------------------------

# System Architecture

Raw TLC Data\
→ Data Processing Pipeline\
→ Cleaned & Enriched Dataset\
→ PostgreSQL Database\
→ Flask REST API\
→ Web Dashboard

------------------------------------------------------------------------

# Backend Implementation

Location: `backend/`

## Data Processing Pipeline

Modules located in `backend/data_processing/`:

### 1. Data Loading (load_data.py)

-   Supports .parquet (trip data)
-   Loads CSV lookup tables
-   Loads GeoJSON metadata

### 2. Data Cleaning (clean_data.py)

The cleaning process performs:

-   Duplicate removal
-   Missing value detection
-   Removal of invalid distances (≤ 0)
-   Removal of invalid fares (≤ 0)
-   Timestamp normalization
-   Trip duration calculation (minutes)
-   Removal of non-positive durations

All excluded records are logged for transparency in:

-   invalid_values.log
-   invalid_duration.log
-   missing_values.log

### 3. Feature Engineering (feature_engineering.py)

Three derived features were engineered:

1.  Trip Duration (minutes)
    -   Derived from pickup and dropoff timestamps
2.  Average Speed (mph)
    -   trip_distance / trip_duration_hours
3.  Fare Per Mile
    -   fare_amount / trip_distance
4.  Pickup Hour
    -   Extracted from pickup timestamp for temporal analysis

These features enable deeper mobility and economic insights.

### 4. Data Enrichment (merge_data.py)

Trip records are merged with: - Pickup zone metadata - Dropoff zone
metadata

This replaces raw LocationIDs with meaningful Borough and Zone
attributes.

------------------------------------------------------------------------

# Database Design

Implemented using PostgreSQL and SQLAlchemy.

## Schema Design

### Fact Table: Trips

-   trip_id (Primary Key)
-   pickup_datetime
-   dropoff_datetime
-   passenger_count
-   trip_distance
-   fare_amount
-   tip_amount
-   total_amount
-   payment_type
-   pickup_location_id
-   dropoff_location_id
-   trip_duration_min
-   avg_speed_mph
-   fare_per_mile
-   pickup_hour

### Dimension Table: Taxi Zones

-   LocationID (Primary Key)
-   Borough
-   Zone
-   Service_Zone

## Indexing Strategy

Indexes applied on: - pickup_datetime - pickup_hour -
pickup_location_id - dropoff_location_id

This enables efficient temporal and geographic queries.

------------------------------------------------------------------------

# Backend API

Framework: Flask\
CORS enabled for frontend integration.

### Endpoint

GET `/api/trips/sample`

Returns enriched trip records including engineered features.

## Running Backend

``` bash
pip install -r requirements.txt
python -m backend.app
```

Default URL: http://localhost:5000

------------------------------------------------------------------------

# Frontend Dashboard

Location: `frontend/`

Technologies: - HTML - CSS - JavaScript

## Features

-   Dynamic API data loading
-   Sorting and filtering by:
    -   Distance
    -   Fare
    -   Duration
    -   Pickup hour
-   Interactive trip summaries
-   Responsive layout

## Running Frontend

``` bash
cd frontend
python -m http.server 5500
```

Access: http://localhost:5500

Ensure backend is running on port 5000.

------------------------------------------------------------------------

# Environment Configuration

`.env` file created in `backend/`:

Install dependencies:

``` bash
pip install flask flask-cors pandas sqlalchemy psycopg2 python-dotenv
```

------------------------------------------------------------------------

# Video Walkthrough

Here is a link to demo video of our application: https://youtu.be/Q9Oy-siY2vI

------------------------------------------------------------------------

# Project Documentation

Find a detailed report of our project in "NYC Taxi Analytics App Documentation.pdf"

------------------------------------------------------------------------

# Project Structure
```

NYC-taxi-analytics/
│
├── .vscode/
│   └── settings.json
├── backend/
│   ├── app.py
│   ├── __init__.py
│   ├── .env
│   ├── routes/
│   │   └── api_routes.py
│   ├── utils/
│   │   └── algorithm.py
│   ├── erd/
│   │   └── erd diagram.jpeg
│   ├── data_processing/
│   │   ├── load_data.py
│   │   ├── clean_data.py
│   │   ├── merge_data.py
│   │   ├── feature_engineering.py
│   │   └── log_utils.py
│   ├── processed_data/
│   │   ├── cleaned_trips_small.csv
│   │   ├── taxi_zone_lookup.csv
│   │   ├── invalid_duration.log
│   │   └── invalid_values.log
│   └── scripts/
│       └── build_db.py
|       └── schema.sql
│
├── frontend/
│   ├── index.html
│   ├── main.js
│   └── style.css
|
├── ca.pem
│
└── README.md

```
------------------------------------------------------------------------

# Engineering Highlights

-   Modular ETL pipeline
-   Transparent anomaly logging
-   Normalized relational schema
-   Indexed database design
-   RESTful API abstraction layer
-   Fullstack integration

------------------------------------------------------------------------

# Conclusion

This project demonstrates a complete enterprise-grade data engineering
and fullstack analytics workflow using real-world urban mobility data.
It integrates data processing, relational modeling, backend API
development, and frontend visualization into a cohesive analytical
system.

### Authors

- Manuelle Ackun
- David Achibiri
- Rhoda Nicole
