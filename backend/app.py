from flask import Flask
from backend.routes.api_routes import api
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

app.register_blueprint(api, url_prefix='/api')

@app.route('/')
def home():
    return "NYC Taxi Data API is running successfully."

if __name__ == '__main__':
    app.run(debug=True)