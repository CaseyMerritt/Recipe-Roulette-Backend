# api_models.py

from flask_restx import fields

def get_models(api):
    recipe_request_model = api.model('Recipe Request', {
        'tags': fields.List(fields.String, required=True, description='List of recipe tags'),
        'count': fields.Integer(description='Number of recipes to return')
    })

    ai_recipe_request_model = api.model('Ai Recipe Request', {
        'ingredients': fields.List(fields.String, required=True, description='List of ingredients'),
        'aiTags': fields.List(fields.String, required=True, description='List of tags')
    })

    return recipe_request_model, ai_recipe_request_model
