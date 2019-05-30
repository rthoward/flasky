import os
import pytest
from sqlalchemy import create_engine, orm
from unittest.mock import Mock

from flasky.app import make_config, make_flask_app, make_routes, make_usecases
import alembic.config
from test import factories


@pytest.fixture(scope="function")
def app(request):
    config = make_config()
    test_config = {**config, "SERVER_NAME": "flasky"}
    app = make_flask_app(test_config)

    # Establish an application context before running the tests.
    ctx = app.app_context()
    ctx.push()

    def teardown():
        ctx.pop()

    request.addfinalizer(teardown)
    return app


@pytest.fixture(scope="session")
def engine():
    config = make_config()
    engine = create_engine(config["SQLALCHEMY_DATABASE_URI"])
    apply_migrations()
    yield engine


class MockSessionHandler(object):
    def __init__(self, session):
        self.session = session


@pytest.fixture(scope="function")
def session_handler(engine, request):
    """Creates a new database session for a test."""
    connection = engine.connect()
    transaction = connection.begin()

    session_factory = orm.sessionmaker(bind=connection)
    Session = orm.scoped_session(session_factory)
    session = Session()
    session_handler = MockSessionHandler(session)

    factory_list = [
        cls
        for _name, cls in factories.__dict__.items()
        if isinstance(cls, type) and cls.__module__ == "test.factories"
    ]
    for factory in factory_list:
        factory._meta.sqlalchemy_session = session
        factory._meta.sqlalchemy_session_persistence = "commit"

    yield session_handler

    def teardown():
        transaction.rollback()
        connection.close()
        Session.remove()

    request.addfinalizer(teardown)
    return session


@pytest.fixture(scope="function")
def session(session_handler):
    return session_handler.session


@pytest.fixture(scope="function")
def routes(app, session_handler):
    usecases = make_usecases(session_handler)
    make_routes(app, usecases)


@pytest.fixture(scope="function")
def mock_session(session_handler):
    return Mock(spec=session_handler.session)


@pytest.fixture(scope="function")
def client(app, routes):
    return app.test_client()


def apply_migrations():
    """Applies all alembic migrations."""
    alembic_config = os.path.join(os.path.dirname(__file__), "../", "alembic.ini")
    config = alembic.config.Config(alembic_config)
    app_config = make_config()
    config.set_main_option("sqlalchemy.url", app_config["SQLALCHEMY_DATABASE_URI"])
    alembic.command.upgrade(config, "head")
