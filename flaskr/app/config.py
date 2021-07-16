"""Flask configuration classes"""


import os


basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS')
    SECRET_KEY = os.getenv('SECRET_KEY')
    SERVER_NAME = os.getenv('SERVER_NAME')
    ELASTICSEARCH_URL = os.getenv('ELASTICSEARCH_URL')

class ConfigDev(Config):
    """Configuration settings for development"""
    DEBUG = os.getenv('DEBUG')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI')
    TEST_DATABASE = 'sqlite:///' + os.path.join(basedir, 'app.db')

class ConfigTest(ConfigDev):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
    TEST = True

config = {
    'development': ConfigDev,
    'testing': ConfigTest
}