from flasky.services import EventService


class CreateHold(object):
    def __init__(self, hold_service, ticket_service):
        self.hold_service = hold_service
        self.ticket_service = ticket_service

    def do(self, user, data):
        data = self.hold_service.cast_create(data)
        return self.hold_service.create(user, **data)
