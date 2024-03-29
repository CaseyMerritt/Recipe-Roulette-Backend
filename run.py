from flask import Flask, request, jsonify
from flask_cors import CORS
from config import DevelopmentConfig, ProductionConfig
from flask_restx import Api, Resource
from models.api_models import get_models  # Import the models
from dotenv import load_dotenv
from firebase_admin import credentials, firestore
import firebase_admin
import random
import openai
import json

load_dotenv()
app = Flask(__name__)
app.config.from_object(DevelopmentConfig)

CORS(app) # Enable CORS

# Initialize Firebase Admin
cred = credentials.Certificate(app.config['FIREBASE_CONFIG_JSON'])
firebase_admin.initialize_app(cred)
db = firestore.client()

# Initialize Openai connection
openai.api_key = app.config['OPENAI_API_KEY']

# Set Up Swagger
api = Api(app, version='1.0', title='Recipe Roulette Backend API', description='Recipe Roulette Backend API')
recipe_request_model, ai_recipe_request_model = get_models(api)
ns = api.namespace('RR', description='Recipe operations')

# Basic Route
@ns.route('/')
class Home(Resource):
    @api.doc(description="Welcome endpoint")
    def get(self):
        """Welcome to the Flask Backend!"""
        return "Welcome to the Flask Backend!"
    

# Basic Test Fetch
@ns.route('/get_data')
class GetData(Resource):
    @api.doc(description="Get sample data")
    def get(self):
        """Fetch sample data"""
        data = {
            "message": "This is a sample response from your Flask API",
            "items": ["item1", "item2", "item3"]
        }
        return jsonify(data)
    

# Get Recipes Function
@ns.route('/get_recipes')
class GetRecipes(Resource):
    @api.expect(recipe_request_model)
    @api.doc(description="Get recipes based on tags", body=recipe_request_model)
    def post(self):
        data = request.get_json()
        tags = data.get('tags')
        count = data.get('count', None)  # Default to None if count is not provided

        if not tags or not isinstance(tags, list):
            return {"Error": "Invalid or missing tags"}, 400

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

            # Check if matching_recipes is empty after the search
            if not matching_recipes:
                return {"Error": "No Recipes Found With Those Tags!"}, 404

            return matching_recipes

        except Exception as e:
            return {"Error": str(e)}, 500


# Get Ai Generated Recipe Function 
@ns.route('/get_ai_recipe')
class GetAIRecipe(Resource):
    @api.expect(ai_recipe_request_model)
    @api.doc(description="Generate a recipe based on ingredients and tags")
    def post(self):
        data = request.get_json()

        if not data:
            return {'Error': 'No data provided'}, 400

        # Check if 'ingredients' and 'tags' are provided and are lists
        if 'ingredients' not in data or not isinstance(data['ingredients'], list):
            return {'Error': 'Ingredients are required and must be a list'}, 400
        if 'aiTags' not in data or not isinstance(data['aiTags'], list):
            return {'Error': 'Tags are required and must be a list'}, 400

        # Join ingredients and tags with ', '
        ingredients = ', '.join(data['ingredients'])
        tags = ', '.join(data['aiTags'])

        print(tags)

        if not ingredients:
            return {'Error': 'Ingredients are not filled out'}, 400
        

        # Try to get GPT's response
        try:
            response = openai.chat.completions.create(
                model="gpt-4", # model="gpt-3.5-turbo",  <= Use for gpt3.5-turbo
                # response_format={ "type": "json_object" }, <= Only for gpt3.5-turbo
                messages=[
                    {"role": "system", "content": "Generate json file with recipe 'title' then 'description' then 'ingredients' then 'steps' that is " + tags + " and contains ONLY the following ingredients and water: " + ingredients + "."}
                ]
            )

            try:
                recipe_data = json.loads(response.choices[0].message.content)

                return recipe_data
            
            except json.JSONDecodeError:
                # If parsing fails, return an error message
                return {"error": "Failed to parse GPT response as JSON", "gpt_response": response}, 500
            
        # Handle exceptions with GPT response
        except Exception as e:
            print(e)
            return {"error": "Failed to get response from GPT", "detail": str(e)}, 500

if __name__ == '__main__':
    app.run(debug=True)
