from flask import Blueprint, jsonify
import pandas as pd
import os

api = Blueprint('api', __name__)

@api.route('/trips/sample', methods=['GET'])
def get_sample_trips():
    try:
        # file path
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        data_path = os.path.join(base_dir, 'processed_data', 'cleaned_trips_small.csv')

        # loading the dataset
        df = pd.read_csv(data_path)

        # renaming columns to match frontend
        df = df.rename(columns={
            'tpep_pickup_datetime': 'pickupTime',
            'tpep_dropoff_datetime': 'dropoffTime',
            'PULocationID': 'pickupLocation',
            'DOLocationID': 'dropoffLocation',
            'trip_distance': 'distance',
            'fare_amount': 'fare',
            'tip_amount': 'tip',
            'total_amount': 'total',
            'payment_type': 'payment',
            'trip_duration_min': 'duration'
        })

        # converting datetime and extracting hours
        df['pickupTime'] = pd.to_datetime(df['pickupTime'], dayfirst=True, errors='coerce')
        df['hour'] = df['pickupTime'].dt.hour

        # creating borough placeholder (temp)
        df['borough'] = df['pickupLocation']

        # creating ID column
        df['id'] = df.index + 1

        # selecting only the fields the frontend needs
        df = df[[
            'id',
            'pickupTime',
            'pickupLocation',
            'dropoffLocation',
            'distance',
            'fare',
            'tip',
            'total',
            'payment',
            'borough',
            'hour'
        ]]

        # converting datetime to string for JSON
        df['pickupTime'] = df['pickupTime'].astype(str)

        return jsonify(df.to_dict(orient='records'))
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500