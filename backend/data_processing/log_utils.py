import os

def log_bad_records(df, filename):
    # logs DataFrame rows that were excluded during cleaning or feature creation
    if df.empty:
        return 
    
    base_dir = os.path.dirname(os.path.dirname(__file__))  
    log_dir = os.path.join(base_dir, "processed_data")

    os.makedirs(log_dir, exist_ok=True)

    file_path = os.path.join(log_dir, filename)
    df.to_csv(file_path, index=False)

    print(f"Logged {len(df)} rows to {file_path}")