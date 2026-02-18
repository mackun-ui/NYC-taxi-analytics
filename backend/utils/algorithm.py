# this file contains custom built algorithms to analyse NYC taxi trip data

def top_earning_trips(trips_list, top_n=10):
    # returns the top N trips with the highest total_amount using a manual sorting algorithm

    if not isinstance(trips_list, list):
        trips_list = trips_list.to_dict(orient="records")
    
    n = len(trips_list)

    # bubble sort in descending order 
    for i in range(n):
        for j in range (0, n - i - 1):
            if trips_list[j]["total_amount"] < trips_list[j + 1]["total_amount"]:
                trips_list[j], trips_list[j + 1] = trips_list[j + 1], trips_list[j]
    
    return trips_list[:top_n]

def group_trips_by_borough(merged_df):
    # groups trips by borough and counts total trips per borough

    borough_counts = {}

    for _, row in merged_df.iterrows():
        borough = row["PU_Borough"]

        if borough not in borough_counts:
            borough_counts[borough] = 0
        
        borough_counts[borough] += 1
    
    return borough_counts

def busiest_zones(merged_df, top_n=10):
    # returns the top N busiest pickup zones based on trip counts

    zone_counts = {}

    for _, row in merged_df.iterrows():
        zone = row["PU_Zone"]

        if zone not in zone_counts:
            zone_counts[zone] = 0
        
        zone_counts[zone] += 1
    
    zone_list = list(zone_counts.items())

    # selection sort
    n = len(zone_list)

    for i in range(n):
        max_idx = i
        for j in range (i + 1, n):
            if zone_list[j][1] > zone_list[max_idx][1]:
                max_idx = j
        
        # this is the swap
        zone_list[i], zone_list[max_idx] = zone_list[max_idx], zone_list[i]

    return zone_list[:top_n]