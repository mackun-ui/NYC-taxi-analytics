from .load_data import load_trip_data, load_zone_lookup
from .clean_data import clean_trip_data
from .merge_data import merge_zone_data

TRIP_FILE = "C:/Users/macku/Downloads/yellow_tripdata_2019-01.csv"
ZONE_FILE = "C:/Users/macku/Downloads/taxi_zone_lookup.csv"

def test_load_and_merge():
    print("Step 1: Loading Data")
    trips_df = load_trip_data(TRIP_FILE)
    zone_df = load_zone_lookup(ZONE_FILE)

    print("\nFirst 5 rows of trip data:")
    print(trips_df.head())

    print("\nFirst 5 rows of zone lookup:")
    print(zone_df.head())

    print("\n Step 2: Cleaning Data")
    cleaned_df = clean_trip_data(trips_df)

    print("\nCleaned data sample:")
    print(cleaned_df.head())

    print("\n Step 3: Merging Zone Data")
    merged_df = merge_zone_data(cleaned_df, zone_df)

    print("\nMerged data sample:")
    print(merged_df[['PULocationID','PU_Borough','PU_Zone',
                     'DOLocationID','DO_Borough','DO_Zone']].head())

    print("\nColumns after merge:")
    print(merged_df.columns)

    print("\nTotal rows after merge:", len(merged_df))

    print("\n Step 4: Exporting Cleaned Data")

    output_path = "backend/processed_data/cleaned_trips.csv"
    cleaned_df.to_csv(output_path, index=False)

    print(f"Cleaned dataset saved to {output_path}")

if __name__ == "__main__":
    test_load_and_merge()
