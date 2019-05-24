from flasky.services import UserService


class CreateUser(object):
    def __init__(self, user_service: UserService):
        self.user_service = user_service

    def do(self, username):
        self.user_service.validate({"username": username})
        return self.user_service.create(username=username)
