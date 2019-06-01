from flasky.services import OrganizationService


class CreateOrganization(object):
    def __init__(self, organization_service: OrganizationService):
        self.organization_service = organization_service

    def do(self, user, data):
        data = self.organization_service.cast(data)
        return self.organization_service.create(user, data)
