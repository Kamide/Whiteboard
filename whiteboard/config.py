import os

class Config(object):
    DEBUG = False
    TESTING = False

class DevelopmentConfig(Config):
    DEBUG = True
    SECRET_KEY = 'development'

class ProductionConfig(Config):
    SECRET_KEY = os.environ.get('SECRET_KEY')
