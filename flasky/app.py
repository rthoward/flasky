from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from flasky.routes import make_routes

from flasky.services import UserService
from flasky.usecases.users import CreateUser


class Usecases(object):
    def __init__(self, user_service):
        self.create_user = CreateUser(user_service)


def make_app(config):
    app = Flask(__name__)
    app.config.update(config)

    db = make_db(app)
    usecases = make_usecases(db.session)
    make_routes(app, usecases)

    return app


def make_db(app):
    return SQLAlchemy(app)


def make_usecases(session):
    return Usecases(UserService(session))


def make_config():
    return {
        "SQLALCHEMY_DATABASE_URI": "postgresql://postgres:postgres@localhost:5432/postgres",
        "SQLALCHEMY_TRACK_MODIFICATIONS": False,
    }
