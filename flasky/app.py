from flask import Flask

from flasky import routes

from flasky.services import UserService
from flasky.routes import make_routes
from flasky.usecases import Usecases
from flasky.util import SessionHandler


def make_app(config):
    app = make_flask_app(config)

    session_handler = SessionHandler(app, make_engine(config))
    usecases = make_usecases(session_handler)
    make_routes(app, usecases)
    return app


def make_usecases(session_handler):
    return Usecases(UserService(session_handler))


def make_flask_app(config):
    app = Flask(__name__)
    app.config.update(config)
    return app


def make_engine(config):
    return sqlalchemy.create_engine(config["SQLALCHEMY_DATABASE_URI"])


def make_config():
    return {
        "SQLALCHEMY_DATABASE_URI": "postgresql://postgres:postgres@localhost:5432/postgres",
        "SQLALCHEMY_TRACK_MODIFICATIONS": False,
    }
