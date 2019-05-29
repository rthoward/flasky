import re

from flasky.services import UserService
from flasky.exceptions import AuthenticationError


class Authenticate(object):
    def __init__(self, user_service: UserService):
        self.user_service = user_service

    def do(self, request, auth_required=False):
        import ipdb; ipdb.set_trace()
        auth_header = request.headers.get("Authorization", "")
        match = re.match(r"Bearer (\w+)", auth_header)

        user_id = None
        if match is not None:
            user_id = match.groups()[0]
        elif auth_required:
            raise AuthenticationError()
        else:
            return None

        return self.user_service.get(user_id)
