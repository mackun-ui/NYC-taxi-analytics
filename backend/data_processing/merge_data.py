def merge_zone_data(df, zone_lookup):
    # merges trips with taxi zone info to attach borough and zone names
    
    # pickup zone info
    df = df.merge(
        zone_lookup.rename(columns={
            'LocationID': 'PULocationID',
            'Borough': 'PU_Borough',
            'Zone': 'PU_Zone'
        }),
        on='PULocationID',
        how='left'
    )

    # dropoff zone info
    df = df.merge(
        zone_lookup.rename(columns={
            'LocationID': 'DOLocationID',
            'Borough': 'DO_Borough',
            'Zone': 'DO_Zone'
        }),
        on='DOLocationID',
        how='left'
    )

    print(df[['PU_Borough', 'DO_Borough']].head())
    print(f"Total rows after merge: {len(df)}")
    return df