import os
import pytest
from flask_sqlalchemy import SQLAlchemy
from unittest.mock import Mock

from flasky.app import make_config, make_flask_app, make_routes
import alembic.config
from test import factories


@pytest.fixture(scope="session")
def app(request):
    config = make_config()
    test_config = {**config, "SERVER_NAME": "meow"}
    app = make_flask_app(test_config)

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
    _db.init_app(app)
    app.db = _db
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

    factory_list = [
        cls
        for _name, cls in factories.__dict__.items()
        if isinstance(cls, type) and cls.__module__ == "test.factories"
    ]
    for factory in factory_list:
        factory._meta.sqlalchemy_session = session
        factory._meta.sqlalchemy_session_persistence = "commit"

    def teardown():
        transaction.rollback()
        connection.close()
        session.remove()

    request.addfinalizer(teardown)
    return session


@pytest.fixture(scope="function", autouse=True)
def _make_routes(app, session):
    make_routes(app)


@pytest.fixture(scope="function")
def mock_session(session):
    return Mock(spec=session)


@pytest.fixture(scope="function")
def client(app, db):
    return app.test_client()


def apply_migrations():
    """Applies all alembic migrations."""
    alembic_config = os.path.join(os.path.dirname(__file__), "../", "alembic.ini")
    config = alembic.config.Config(alembic_config)
    app_config = make_config()
    config.set_main_option("sqlalchemy.url", app_config["SQLALCHEMY_DATABASE_URI"])
    alembic.command.upgrade(config, "head")
