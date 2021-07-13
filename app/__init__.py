from .config import Config
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from elasticsearch import Elasticsearch
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
app.elasticsearch = Elasticsearch([app.config['ELASTICSEARCH_URL']]) \
    if app.config['ELASTICSEARCH_URL'] else None

from app import models, views
from app.swagger import swaggerui_blueprint

from app.api import bp as api_bp
app.register_blueprint(api_bp, url_prefix='/api')
app.register_blueprint(views.views, url_prefix='/')
app.register_blueprint(swaggerui_blueprint)
