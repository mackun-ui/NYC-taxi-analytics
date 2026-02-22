from flask import Blueprint, jsonify, current_app
from sqlalchemy import text

api = Blueprint('api', __name__)

@api.route('/trips/sample', methods=['GET'])
def get_sample_trips():
    try:
        engine = current_app.config['ENGINE']

        query = text("""
            SELECT 
                t."VendorID" as id,
                TO_CHAR(
                    TO_TIMESTAMP(t."tpep_pickup_datetime", 'DD/MM/YYYY HH24:MI'),
                    'YYYY-MM-DD"T"HH24:MI:SS'
                ) as "pickupTime",
                t."PULocationID" as "pickupLocation",
                t."DOLocationID" as "dropoffLocation",
                t."trip_distance" as distance,
                t."fare_amount" as fare,
                t."tip_amount" as tip,
                t."total_amount" as total,
                t."payment_type" as payment,
                t."trip_duration_min" as duration,
                EXTRACT(HOUR FROM TO_TIMESTAMP(t."tpep_pickup_datetime", 'DD/MM/YYYY HH24:MI')) as hour,
                z."Borough" as borough
            FROM trips t
            LEFT JOIN taxi_zones z
            ON t."PULocationID" = z."LocationID"
            LIMIT 1000
        """)


        with engine.connect() as conn:
            result = conn.execute(query)
            rows = result.fetchall()

        # payment labels expected from frontend
        payment_map = {
            1: "Credit Card",
            2: "Cash",
            3: "No Charge",
            4: "Dispute",
            5: "Unknown",
            6: "Voided"
        }

        # convert to list of dicts
        data = []
        for row in rows:
            record = dict(row._mapping)

            # convert payment type code to label
            record["payment"] = payment_map.get(record["payment"], "Other")

            data.append(record)

        return jsonify(data)

    except Exception as e:
        print("API ERROR:", str(e))
        return jsonify({'error': str(e)}), 500
