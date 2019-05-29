from flask import Flask

from flasky import routes

from flasky.services import UserService
from flasky.routes import make_routes
from flasky.usecases import Usecases

import sqlalchemy

class SessionHandler(object):
    def __init__(self, app: Flask, engine: sqlalchemy.engine.Engine):
        self.app = app
        self.engine = engine

        self.session = self.create_scoped_session()

        self.init_context_handlers()

    def create_scoped_session(self):
        return sqlalchemy.orm.scoped_session(self.session_factory())

    def session_factory(self):
        return sqlalchemy.orm.sessionmaker(bind=self.engine)

    def init_context_handlers(self):

        @self.app.teardown_appcontext
        def shutdown_session(response_or_exc):
            self.session.remove()
            return response_or_exc


def make_flask_app(config, session_handler=SessionHandler):
    app = Flask(__name__)
    app.config.update(config)

    session_handler = SessionHandler(app, make_engine(config))
    usecases = Usecases(UserService(session_handler))
    make_routes(app, usecases)
    return app


def make_engine(config):
    return sqlalchemy.create_engine(config["SQLALCHEMY_DATABASE_URI"])


def make_config():
    return {
        "SQLALCHEMY_DATABASE_URI": "postgresql://postgres:postgres@localhost:5432/postgres",
        "SQLALCHEMY_TRACK_MODIFICATIONS": False,
    }
