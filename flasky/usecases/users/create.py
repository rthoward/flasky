from flasky.services import UserService


class CreateUser(object):
    def __init__(self, user_service: UserService):
        self.user_service = user_service

    def do(self, data):
        data = self.user_service.cast(data)
        return self.user_service.create(data)
