from .users import CreateUser
from .auth import Authenticate


class Usecases(object):
    def __init__(self, user_service):
        self.create_user = CreateUser(user_service)
        self.auth = Authenticate(user_service)
