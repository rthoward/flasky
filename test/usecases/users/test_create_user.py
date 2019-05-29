import pytest

from flasky.usecases.users import CreateUser
from flasky.services.user_service import UserService
from flasky.validator import ValidationError
from test import testutils


@pytest.fixture
def create_user(session_handler) -> CreateUser:
    return CreateUser(UserService(session_handler=session_handler))


def test_create_user(create_user: CreateUser):
    new_user = create_user.do("username")

    assert new_user.id
    assert new_user.username == "username"


def test_create_user_with_long_username(create_user: CreateUser):
    long_username = str(["a"] * 100)
    testutils.assert_validation_errors(
        ["username"], lambda: create_user.do(long_username)
    )


def test_create_user_with_existing_username(create_user: CreateUser):
    create_user.do("a")
    create_user.do("a")
