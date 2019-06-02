from typing import List
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import IntegrityError

from flasky.models import Hold
from flasky.exceptions import NotFoundError, ConflictError, MissingOrganizationError
from flasky.serializers import HoldRequestSerializer


class HoldService(object):
    def __init__(self, session_handler):
        self.session_handler = session_handler

    @property
    def session(self):
        return self.session_handler.session

    def create(self, user, event_id, quantity) -> Hold:
        hold = Hold(user=user, event_id=event_id, quantity=quantity)
        self.session.add(hold)
        self.session.commit()

        return hold

    def get(self, id_: int) -> Hold:
        try:
            return self.session.query(Hold).filter_by(id=id_).one()
        except NoResultFound:
            raise NotFoundError("hold", id_)

    def list(self) -> List[Hold]:
        return self.session.query(Hold).all()

    def cast_create(self, d: dict) -> dict:
        return HoldRequestSerializer().load(d)
