# api_models.py

from flask_restx import fields

def get_models(api):

    recipe_model = api.model('Recipe', {

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
        'email' : fields.String(required=True, description='Email to send to'),
        'recipes' : fields.List(fields.String(required=True, description='List of recipe objects'))
    })

    return recipe_request_model, ai_recipe_request_model, send_email_model
