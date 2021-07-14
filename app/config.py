import os

basedir = os.path.abspath(os.path.dirname(__file__))

class ConfigDev:
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI') #or 'postgresql://postgres:root@db:5432/postgres'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SECRET_KEY = os.getenv('SECRET_KEY') or 'you-will-never-guess'
    SERVER_NAME = '0.0.0.0:80'
    ELASTICSEARCH_URL = os.getenv('ELASTICSEARCH_URL')
