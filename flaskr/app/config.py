"""Flask configuration classes"""


import os


basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS')
    SECRET_KEY = os.getenv('SECRET_KEY')
    SERVER_NAME = os.getenv('SERVER_NAME')
    ELASTICSEARCH_URL = os.getenv('ELASTICSEARCH_URL')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI')
    LOG_TO_STDOUT = os.getenv('LOG_TO_STDOUT')


class ConfigDev(Config):
    """Configuration settings for development"""
    DEBUG = os.getenv('DEBUG')


class ConfigTest(ConfigDev):
    """Configuration settings for development"""
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
    TEST = True


class ConfigProd(Config):
    """Configuration settings for production"""
    LOG_TO_STDOUT = os.getenv('LOG_TO_STDOUT')


config = {
    'development': ConfigDev,
    'testing': ConfigTest,
    'production': ConfigProd
}
