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
        'projectId': os.environ.get('FIREBASE_PROJECT_ID_DEV'),
        'storageBucket': os.environ.get('FIREBASE_STORAGE_BUCKET'),
        'messagingSenderId' : os.environ.get('FIREBASE_MESSAGING_SENDER_ID'),
        'appId': os.environ.get('FIREBASE_APP_ID'),
        'measurementId': os.environ.get('FIREBASE_MEASUREMENT_ID')
    }

class ProductionConfig(Config):
    # Production-specific configurations
    OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY_PROD')
    FIREBASE_CONFIG = {
        'apiKey': os.environ.get('FIREBASE_API_KEY_PROD'),
        'authDomain': os.environ.get('FIREBASE_AUTH_DOMAIN_PROD'),
        # Include other necessary Firebase config variables
    }
