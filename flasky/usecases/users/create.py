from flasky.services import UserService


class CreateUser(object):
    def __init__(self, user_service: UserService):
        self.user_service = user_service

    def do(self, data):
        changeset = self.user_service.changeset(data)
        return self.user_service.create(changeset)
