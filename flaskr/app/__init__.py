"""Application initialization"""


from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from elasticsearch import Elasticsearch
from flask_migrate import Migrate
from .config import ConfigDev

db = SQLAlchemy()
migrate = Migrate()


def create_app():
    """Application factory pattern"""
    app = Flask(__name__)
    app.config.from_object(ConfigDev)

    db.init_app(app)
    migrate.init_app(app)

    app.elasticsearch = Elasticsearch([app.config['ELASTICSEARCH_URL']]) \
        if app.config['ELASTICSEARCH_URL'] else None

    from app import models
    from app.swagger import swaggerui_blueprint

    from app.api import bp as api_bp
    app.register_blueprint(api_bp, url_prefix='/api')
    app.register_blueprint(swaggerui_blueprint)

    return app
