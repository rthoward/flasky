from typing import List
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import IntegrityError

from flasky.models import Ticket


class TicketService(object):
    def __init__(self, session_handler):
        self.session_handler = session_handler

    @property
    def session(self):
        return self.session_handler.session

    def create(self,) -> Ticket:
        pass

    def get(self, id_: int) -> Ticket:
        try:
            return self.session.query(Ticket).filter_by(id=id_).one()
        except NoResultFound:
            raise NotFoundError("ticket", id_)

    def list(self) -> List[Ticket]:
        return self.session.query(Ticket).all()

    def cast_request(self, d: dict) -> dict:
        return TicketRequestSerializer().load(d)
