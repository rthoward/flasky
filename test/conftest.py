import os
import pytest
from flask_sqlalchemy import SQLAlchemy
from unittest.mock import Mock

from flasky.app import make_config, make_app
import alembic.config


@pytest.fixture(scope="session")
def app(request):
    config = make_config()
    app = make_app(config)

    # Establish an application context before running the tests.
    ctx = app.app_context()
    ctx.push()

    def teardown():
        ctx.pop()

    request.addfinalizer(teardown)
    return app


@pytest.fixture(scope="session")
def db(app, request):
    _db = SQLAlchemy()
    _db.app = app
    apply_migrations()
    yield _db
    _db.drop_all()


@pytest.fixture(scope="function")
def session(db, request):
    """Creates a new database session for a test."""
    connection = db.engine.connect()
    transaction = connection.begin()

    options = dict(bind=connection, binds={})
    session = db.create_scoped_session(options=options)

    db.session = session

    def teardown():
        transaction.rollback()
        connection.close()
        session.remove()

    request.addfinalizer(teardown)
    return session


@pytest.fixture(scope="function")
def mock_session(session):
    return Mock(spec=session)


def apply_migrations():
    """Applies all alembic migrations."""
    alembic_config = os.path.join(os.path.dirname(__file__), "../", "alembic.ini")
    config = alembic.config.Config(alembic_config)
    app_config = make_config()
    config.set_main_option("sqlalchemy.url", app_config["SQLALCHEMY_DATABASE_URI"])
    alembic.command.upgrade(config, "head")
