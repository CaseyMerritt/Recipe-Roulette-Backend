# api_models.py

from flask_restx import fields

def get_models(api):
    # Define an ingredient model as each ingredient is a map with name, quantity, and unit
    ingredient_model = api.model('Ingredient', {
        'name': fields.String(required=True, description='Name of the ingredient'),
        'quantity': fields.String(required=True, description='Quantity of the ingredient'),
        'unit': fields.String(required=True, description='Unit of measurement')
    })

    # Define a macronutrient model as it is represented by a map
    macronutrient_model = api.model('Macronutrient', {
        'calories': fields.Integer(required=True, description='Calories per serving'),
        'protein': fields.String(required=True, description='Protein content per serving'),
        'carbs': fields.String(required=True, description='Carbohydrates content per serving'),
        'fat': fields.String(required=True, description='Fat content per serving')
    })

    # Define the complete recipe model
    recipe_model = api.model('Recipe', {
        'title': fields.String(required=True, description='Title of the recipe'),
        'description': fields.String(required=True, description='Description of the recipe'),
        'instructions': fields.List(fields.String, required=True, description='Cooking instructions'),
        'ingredients': fields.List(fields.Nested(ingredient_model), required=True, description='List of ingredients'),
        'macronutrients': fields.Nested(macronutrient_model, required=True, description='Nutritional information'),
        'tags': fields.List(fields.String, required=True, description='Tags associated with the recipe')
    })

    recipe_request_model = api.model('Recipe Request', {
        'tags': fields.List(fields.String, required=True, description='List of recipe tags'),
        'count': fields.Integer(description='Number of recipes to return')
    })

    ai_recipe_request_model = api.model('Ai Recipe Request', {
        'ingredients': fields.List(fields.String, required=True, description='List of ingredients'),
        'aiTags': fields.List(fields.String, required=True, description='List of tags')
    })

    send_email_model = api.model('Send Email Request', {
        'email': fields.String(required=True, description='Email to send to'),
        'recipes': fields.List(fields.Nested(recipe_model), required=True, description='List of recipe objects to send')
    })

    return recipe_model, recipe_request_model, ai_recipe_request_model, send_email_model

