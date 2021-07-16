"""Flask configuration classes"""


import os


basedir = os.path.abspath(os.path.dirname(__file__))


class ConfigDev:
    """Configuration settings for development"""
    DEBUG = os.getenv('DEBUG')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS')
    SECRET_KEY = os.getenv('SECRET_KEY')
    SERVER_NAME = os.getenv('SERVER_NAME')
    ELASTICSEARCH_URL = os.getenv('ELASTICSEARCH_URL')
    TEST_DATABASE = 'sqlite:///' + os.path.join(basedir, 'app.db')

class ConfigTest(ConfigDev):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
