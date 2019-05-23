from flasky.models import User


class InvalidUsernameException(Exception):
    pass


class UserService(object):
    def __init__(self, session):
        self.session = session

    def create(self, username):
        if len(username) > 50:
            raise InvalidUsernameException()

        new_user = User(username=username)
        self.session.add(new_user)
        self.session.commit()

        return new_user
