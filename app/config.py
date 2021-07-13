import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI') or \
            'postgresql://' + os.path.join('postgres:pass@localhost:5432/postgres')
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SERVER_NAME = 'localhost:5000'
    ELASTICSEARCH_URL = 'http://localhost:9200'#os.environ.get('ELASTICSEARCH_URL')
