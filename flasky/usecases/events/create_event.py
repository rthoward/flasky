from flasky.services import EventService


class CreateEvent(object):
    def __init__(self, event_service: EventService):
        self.event_service = event_service

    def do(self, user, data):
        data = self.event_service.cast(data)
        return self.event_service.create(user, data)
