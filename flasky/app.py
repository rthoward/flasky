from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from flasky.routes import make_routes
from flasky.services import UserService
from flasky.usecases import Usecases


def make_app(config, session=None):
    app = Flask(__name__)
    app.config.update(config)

    session = make_session(app)
    usecases = make_usecases(session)
    make_routes(app, usecases)

    return app


def make_session(app):
    db = SQLAlchemy(app)
    return db.session


def make_usecases(session):
    return Usecases(UserService(session))


def make_config():
    return {
        "SQLALCHEMY_DATABASE_URI": "postgresql://postgres:postgres@localhost:5432/postgres",
        "SQLALCHEMY_TRACK_MODIFICATIONS": False,
    }
