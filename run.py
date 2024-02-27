from flask import Flask, request, jsonify
from flask_cors import CORS
from config import DevelopmentConfig, ProductionConfig

import firebase_admin
from firebase_admin import credentials, firestore
import random


from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
# Enable CORS for all routes and origins
CORS(app)

app.config.from_object(DevelopmentConfig)

# Initialize Firebase Admin
cred = credentials.Certificate((jsonify(app.config['FIREBASE_CONFIG'])))
firebase_admin.initialize_app(cred)

# Get a reference to the Firestore service
db = firestore.client()

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

@app.route('/get_recipes', methods=['POST'])
def get_recipes():
    data = request.get_json()
    tagged = data.get('tagged')
    count = data.get('count', None)  # Default to None if count is not provided

    if not tagged or not isinstance(tagged, list):
        return jsonify({'error': 'Invalid or missing tags'}), 400

    try:
        recipes_ref = db.collection('recipes')
        matching_recipes = []
        for tag in tagged:
            query = recipes_ref.where('tags', 'array_contains', tag).stream()
            for doc in query:
                if doc.id not in [recipe['id'] for recipe in matching_recipes]:
                    recipe = doc.to_dict()
                    recipe['id'] = doc.id
                    matching_recipes.append(recipe)

        # If a count is provided and is less than the number of matching recipes,
        # randomly select 'count' recipes from the list of matching recipes
        if count is not None and 0 < count < len(matching_recipes):
            matching_recipes = random.sample(matching_recipes, count)

        return jsonify(matching_recipes)

    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
