from .load_data import load_trip_data, load_zone_lookup
from .clean_data import clean_trip_data
from .merge_data import merge_zone_data

TRIP_FILE = "C:/Users/macku/Downloads/yellow_tripdata_2019-01.csv"
ZONE_FILE = "C:/Users/macku/Downloads/taxi_zone_lookup.csv"

def test_load_and_merge():
    print("---- STEP 1: LOADING DATA ----")
    trips_df = load_trip_data(TRIP_FILE)
    zone_df = load_zone_lookup(ZONE_FILE)

    print("\nFirst 5 rows of trip data:")
    print(trips_df.head())

    print("\nFirst 5 rows of zone lookup:")
    print(zone_df.head())

    print("\n---- STEP 2: CLEANING DATA ----")
    cleaned_df = clean_trip_data(trips_df)

    print("\nCleaned data sample:")
    print(cleaned_df.head())

    print("\n---- STEP 3: MERGING ZONE DATA ----")
    merged_df = merge_zone_data(cleaned_df, zone_df)

    print("\nMerged data sample:")
    print(merged_df[['PULocationID','PU_Borough','PU_Zone',
                     'DOLocationID','DO_Borough','DO_Zone']].head())

    print("\nColumns after merge:")
    print(merged_df.columns)

    print("\nTotal rows after merge:", len(merged_df))


if __name__ == "__main__":
    test_load_and_merge()
