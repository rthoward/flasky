from typing import List
from sqlalchemy.orm.exc import NoResultFound

from flasky.models import User
from flasky.exceptions import NotFoundError
from flasky.serializers import UserSerializer


class UserService(object):
    def __init__(self, session_handler):
        self.session_handler = session_handler

    @property
    def session(self):
        return self.session_handler.session

    def create(self, data) -> User:
        new_user = User(**data)
        self.session.add(new_user)
        self.session.commit()

        return new_user

    def get(self, id_: int) -> User:
        try:
            return self.session.query(User).filter_by(id=id_).one()
        except NoResultFound:
            raise NotFoundError("user", id_)

    def list(self) -> List[User]:
        return self.session.query(User).all()

    def cast(self, user_dict: dict) -> dict:
        return UserSerializer().load(user_dict)
