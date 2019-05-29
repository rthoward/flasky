from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

from flasky.routes import make_routes
from flasky.services import UserService
from flasky.usecases import Usecases


def make_app(config, session=None):
    app = Flask(__name__)
    app.config.update(config)

    session = session or make_session(config)
    usecases = make_usecases(session)
    make_routes(app, usecases)
    make_handlers(app, session)

    return app


def make_session(config):
    engine = create_engine(config["SQLALCHEMY_DATABASE_URI"])
    session_factory = sessionmaker(bind=engine)
    return scoped_session(session_factory)()


def make_handlers(app, session):
    pass
    # @app.teardown_appcontext
    # def teardown_appcontext(response_or_exc):
    #     session.remove()


def make_usecases(session):
    return Usecases(UserService(session))


def make_config():
    return {
        "SQLALCHEMY_DATABASE_URI": "postgresql://postgres:postgres@localhost:5432/postgres",
        "SQLALCHEMY_TRACK_MODIFICATIONS": False,
    }
