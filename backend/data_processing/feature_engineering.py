def add_features(df):
    #adds avg_speed_mph, fare_per_mile, and pickup_hour to cleaned DataFrame

    df = df.copy()
    df['trip_duration_hrs'] = df['trip_duration_min'] / 60

    df['avg_speed_mph'] = df['trip_distance'] / df['trip_duration_hrs']
    df['fare_per_mile'] = df['fare_amount'] / df['trip_distance']
    df['pickup_hour'] = df['tpep_pickup_datetime'].dt.hour

    # drop temporary column
    df.drop(columns=['trip_duration_hrs'], inplace=True)

    return df