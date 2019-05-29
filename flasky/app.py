from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from flasky import routes

from flasky.services import UserService
from flasky.usecases import Usecases


def make_flask_app(config):
    app = Flask(__name__)
    app.config.update(config)
    make_db(app)
    return app


def make_routes(app):
    usecases = make_usecases(app.db.session)
    routes.make_routes(app, usecases)


def make_db(app):
    db = SQLAlchemy(app)
    app.db = db


def make_usecases(session):
    return Usecases(UserService(session))


def make_config():
    return {
        "SQLALCHEMY_DATABASE_URI": "postgresql://postgres:postgres@localhost:5432/postgres",
        "SQLALCHEMY_TRACK_MODIFICATIONS": False,
    }
