import pytest
from unittest.mock import Mock
from flask_sqlalchemy import SQLAlchemy

from flasky.models.user import User
from flasky.services.user_service import UserService, InvalidUsernameException


def test_create_user(session):
    new_user = UserService(session).create(username="username")
    assert session.query(User).get(new_user.id)


def test_create_user_validates_name_length(mock_session):
    long_username = ''.join(["a"] * 100)

    user_service = UserService(session=mock_session)

    with pytest.raises(InvalidUsernameException):
        user_service.create(username=long_username)

    mock_session.assert_not_called()
