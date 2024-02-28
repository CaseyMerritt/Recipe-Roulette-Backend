from flask import Flask, request, jsonify
from flask_cors import CORS
from config import DevelopmentConfig, ProductionConfig

import firebase_admin
from firebase_admin import credentials, firestore
import random

import openai


from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
# Enable CORS for all routes and origins
CORS(app)

app.config.from_object(DevelopmentConfig)

# Initialize Firebase Admin
cred = credentials.Certificate(app.config['FIREBASE_CONFIG_JSON'])
firebase_admin.initialize_app(cred)

# Initialize Openai connection
openai.api_key = app.config['OPENAI_API_KEY']

# Get a reference to the Firestore service
db = firestore.client()

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
    tags = data.get('tags')
    count = data.get('count', None)  # Default to None if count is not provided

    if not tags or not isinstance(tags, list):
        return jsonify({'error': 'Invalid or missing tags'}), 400

    try:
        recipes_ref = db.collection('recipes')
        matching_recipes = []
        for tag in tags:
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
    
@app.route('/get_ai_recipe', methods=['POST'])
def get_ai_recipe():
    data = request.get_json()

    if not data:
        return jsonify({'error': 'No data provided'}), 400

    # Check if 'ingredients' and 'tags' are provided and are lists
    if 'ingredients' not in data or not isinstance(data['ingredients'], list):
        return jsonify({'error': 'Ingredients are required and must be a list'}), 400
    if 'tags' not in data or not isinstance(data['tags'], list):
        return jsonify({'error': 'Tags are required and must be a list'}), 400

    # Join ingredients and tags with ', '
    ingredients = ', '.join(data['ingredients'])
    tags = ', '.join(data['tags'])

    try:
        response = openai.ChatCompletion.create(
            model="Recipe Maker",  # Replace "Recipe Maker" with a valid model identifier
            messages=[
                {"role": "system", "content": "Generate a Recipe that is " + tags + " and contains the following ingredients: " + ingredients + "."}
            ]
        )
    except Exception as e:
        return jsonify({'error': 'Failed to generate recipe', 'details': str(e)}), 500

    return jsonify({'recipe': response.choices[0].message['content']})


if __name__ == '__main__':
    app.run(debug=True)
