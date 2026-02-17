from flask import Flask
from .routes.api_routes import api

app = Flask(__name__)
app.register_blueprint(api, url_prefix='/api')

@app.route('/')
def home():
    return "NYC Taxi Data API is running successfully."

if __name__ == '__main__':
    app.run(debug=True)