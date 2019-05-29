from flask import Flask
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
