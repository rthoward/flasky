from flasky.models import User
from flasky.validator import Validator


CREATE_USER_SCHEMA = {
    "username": {"nullable": False, "type": "string", "maxlength": 50}
}


class UserService(object):
    def __init__(self, session):
        self.session = session

    def create(self, username) -> User:
        new_user = User(username=username)
        self.session.add(new_user)
        self.session.commit()

        return new_user

    def validate(self, user_dict: dict):
        Validator(CREATE_USER_SCHEMA).validate(user_dict)
