from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from flasky.routes import make_routes

def make_app(config):
    app = Flask(__name__)
    app.config.update(config)

    db = make_db(app)
    make_routes(app)

    return app


def make_db(app):
    return SQLAlchemy(app)


def make_config():
    return {
        "SQLALCHEMY_DATABASE_URI": "postgres://postgres:postgres@localhost:5432/postgres"
    }
