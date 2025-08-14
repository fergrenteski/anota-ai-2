import os
from decouple import config

class Config:
    SECRET_KEY = config('SECRET_KEY', default='dev-secret-key')
    SQLALCHEMY_DATABASE_URI = config('DATABASE_URL', default='sqlite:///data/anota_ai.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = config('SQLALCHEMY_ECHO', default=False, cast=bool)

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_ECHO = True

class ProductionConfig(Config):
    DEBUG = False

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False

config_dict = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig
}

def get_config():
    return config_dict.get(config('FLASK_ENV', default='development'), DevelopmentConfig)
