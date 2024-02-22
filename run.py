from flask import Flask, jsonify
from flask_cors import CORS
from config import DevelopmentConfig, ProductionConfig


from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
# Enable CORS for all routes and origins
CORS(app)

app.config.from_object("config.DevelopmentConfig")

#if app.env == "production":
    #app.config.from_object("config.ProductionConfig")
#else:
    #app.config.from_object("config.DevelopmentConfig")

@app.route('/')
def home():
    return "Welcome to the Flask Backend!"

@app.route('/get_data')
def get_data():
    # Example data
    data = {
        "message": "This is a sample response from your Flask API",
        "items": ["item1", "item2", "item3"]
    }
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
