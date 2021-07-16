"""Command line interface for flask"""

import click

from flask import current_app
from app.dev_database import init_database
from app import db


def register(app):
    @app.cli.group()
    def seed():
        """Seeding and resetting database"""
        pass

    @seed.command()
    def create_db():
        db.create_all()

    @seed.command()
    def init():
        """DB initialization"""
        init_database()
