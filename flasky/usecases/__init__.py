from .users import CreateUser, ListUsers
from .auth import Authenticate
from .organizations import CreateOrganization
from .events import CreateEvent


class Usecases(object):
    def __init__(self, user_service, organization_service, event_service):
        self.create_user = CreateUser(user_service)
        self.list_users = ListUsers(user_service)
        self.auth = Authenticate(user_service)
        self.create_organization = CreateOrganization(organization_service)
        self.create_event = CreateEvent(event_service)
