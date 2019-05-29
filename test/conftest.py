import os
import pytest
from unittest.mock import Mock
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
import contextlib

from flasky.app import make_config, make_app, make_session
import alembic.config
from test import factories


@pytest.fixture(scope="function")
def app(request, config, session):
    app = make_app(config, session=session)

    # Establish an application context before running the tests.
    ctx = app.app_context()
    ctx.push()

    def teardown():
        ctx.pop()

    request.addfinalizer(teardown)
    return app


@pytest.fixture(scope="session")
def config():
    config = make_config()
    config.update({"SERVER_NAME": "meow"})
    return config


@pytest.fixture(scope="session")
def engine(request, config):
    engine = create_engine(config["SQLALCHEMY_DATABASE_URI"])
    apply_migrations()
    return engine


@pytest.fixture(scope="function", autouse=True)
def session(engine, request):
    """Creates a new database session for a test."""

    connection = engine.connect()
    transaction = connection.begin()

    options = dict(bind=connection, binds={})
    session_factory = sessionmaker(bind=engine)
    Session = scoped_session(session_factory)

    session_ = Session()

    factory_list = [
        cls
        for _name, cls in factories.__dict__.items()
        if isinstance(cls, type) and cls.__module__ == "test.factories"
    ]
    for factory in factory_list:
        factory._meta.sqlalchemy_session = session_
        factory._meta.sqlalchemy_session_persistence = "commit"

    def teardown():
        transaction.rollback()
        connection.close()
        Session.remove()

    request.addfinalizer(teardown)
    return session_


@pytest.fixture(scope="function")
def mock_session(session):
    return Mock(spec=session)


@pytest.fixture(scope="function")
def client(app):
    return app.test_client()


def apply_migrations():
    """Applies all alembic migrations."""
    alembic_config = os.path.join(os.path.dirname(__file__), "../", "alembic.ini")
    config = alembic.config.Config(alembic_config)
    app_config = make_config()
    config.set_main_option("sqlalchemy.url", app_config["SQLALCHEMY_DATABASE_URI"])
    alembic.command.upgrade(config, "head")
