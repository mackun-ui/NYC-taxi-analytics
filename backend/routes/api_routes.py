from flask import Blueprint, jsonify
import pandas as pd
import os

api = Blueprint('api', __name__)

# load the processed data
data_path = os.path.join(os.path.dirname(__file__), '..', 'processed_data', 'cleaned_trips_small.csv')

if not os.path.exists(data_path):
    raise FileNotFoundError(f"CSV not found at {data_path}")

df = pd.read_csv(data_path)

@api.route('/trips/sample', methods=['GET'])
def get_sample_trips():
    # returns a sample of 100 trips for frontend testing

    sample = df.sample(100, random_state=42).to_dict(orient='records')
    return jsonify(sample)