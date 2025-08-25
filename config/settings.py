import os
from decouple import config

# Caminho base do projeto
BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data')

# Garantir que o diretório data existe
os.makedirs(DATA_DIR, exist_ok=True)

class Config:
    SECRET_KEY = config('SECRET_KEY', default='dev-secret-key')
    # Usar caminho absoluto para o banco de dados
    DB_PATH = os.path.join(DATA_DIR, "anota_ai.db")
    SQLALCHEMY_DATABASE_URI = config('DATABASE_URL', default=f'sqlite:///{DB_PATH}')
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
