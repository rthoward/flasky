from .users import CreateUser, ListUsers
from .auth import Authenticate


class Usecases(object):
    def __init__(self, user_service):
        self.create_user = CreateUser(user_service)
        self.list_users = ListUsers(user_service)
        self.auth = Authenticate(user_service)
