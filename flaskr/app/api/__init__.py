"""Create blueprint for api"""

from flask import Blueprint

bp = Blueprint('api', __name__)

from app.api import users, directors, errors, genres, movies, tokens
