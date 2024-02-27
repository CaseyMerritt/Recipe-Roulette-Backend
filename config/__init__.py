import os

class Config:
    # General config
    SECRET_KEY = os.environ.get('SECRET_KEY')

class DevelopmentConfig(Config):
    # Development-specific configurations
    OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY_DEV')
    FIREBASE_CONFIG_JSON = 'firebase_auth.json'

class ProductionConfig(Config):
    # Production-specific configurations
    OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY_PROD')
    FIREBASE_CONFIG_JSON = 'firebase_auth.json'
