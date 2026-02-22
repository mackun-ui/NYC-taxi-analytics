from flask import Flask
from backend.routes.api_routes import api
from flask_cors import CORS
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv

# load env file
load_dotenv()

app = Flask(__name__)
CORS(app)

# DB connection
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)

# make engine accessible in routes
app.config['ENGINE'] = engine

app.register_blueprint(api, url_prefix='/api')

@app.route('/')
def home():
    return "NYC Taxi Data API is running successfully."

if __name__ == '__main__':
    app.run(debug=True)