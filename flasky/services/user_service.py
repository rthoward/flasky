from flasky.models import User


class UserService(object):
    def __init__(self, session):
        self.session = session

    def create(self, username):
        new_user = User(username=username)
        self.session.add(new_user)
        self.session.commit()

        return new_user

