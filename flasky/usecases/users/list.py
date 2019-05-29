from typing import List

from flasky.services import UserService
from flasky.models import User


class ListUsers(object):
    def __init__(self, user_service: UserService):
        self.user_service = user_service

    def do(self) -> List[User]:
        return self.user_service.list()
