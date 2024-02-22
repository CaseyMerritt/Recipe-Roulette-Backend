import os

class Config:
    # General config
    SECRET_KEY = os.environ.get('SECRET_KEY')

class DevelopmentConfig(Config):
    # Development-specific configurations
    OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY_DEV')
    FIREBASE_CONFIG = {
        'apiKey': os.environ.get('FIREBASE_API_KEY_DEV'),
        'authDomain': os.environ.get('FIREBASE_AUTH_DOMAIN_DEV'),
        # Include other necessary Firebase config variables
    }

class ProductionConfig(Config):
    # Production-specific configurations
    OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY_PROD')
    FIREBASE_CONFIG = {
        'apiKey': os.environ.get('FIREBASE_API_KEY_PROD'),
        'authDomain': os.environ.get('FIREBASE_AUTH_DOMAIN_PROD'),
        # Include other necessary Firebase config variables
    }
