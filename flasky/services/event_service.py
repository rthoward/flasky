from typing import List
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import IntegrityError

from flasky.models import Event
from flasky.exceptions import NotFoundError, ConflictError, MissingOrganizationError
from flasky.serializers import EventSerializer

from psycopg2 import errors


class EventService(object):
    def __init__(self, session_handler):
        self.session_handler = session_handler

    @property
    def session(self):
        return self.session_handler.session

    def create(self, user, data) -> Event:
        if not user.in_organization:
            raise MissingOrganizationError()

        event = Event(organization=user.organization, **data)
        self.session.add(event)

        try:
            self.session.commit()
            return event
        except IntegrityError:
            raise ConflictError("event")

    def get(self, id_: int) -> Event:
        try:
            return self.session.query(Event).filter_by(id=id_).one()
        except NoResultFound:
            raise NotFoundError("event", id_)

    def list(self) -> List[Event]:
        return self.session.query(Event).all()

    def cast(self, d: dict) -> dict:
        return EventSerializer().load(d)
