from flasky.services import UserService

class CreateUser(object):
    def __init__(self, user_service: UserService):
        self.user_service = user_service

    def do(self, username):
        user = self.user_service.create(username=username)
        return user
