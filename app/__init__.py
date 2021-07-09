from .config import Config
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app import models, views
from app.swagger import swaggerui_blueprint

app.register_blueprint(views.views, url_prefix='/')
app.register_blueprint(swaggerui_blueprint)
