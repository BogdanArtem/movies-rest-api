from .config import Config
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app import models, views

from app.api import bp as api_bp
app.register_blueprint(api_bp, url_prefix='/api')
app.register_blueprint(views.views, url_prefix='/')
