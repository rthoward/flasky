from typing import List
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import IntegrityError

from flasky.models import Organization
from flasky.exceptions import NotFoundError, ConflictError
from flasky.serializers import OrganizationSerializer


class OrganizationService(object):
    def __init__(self, session_handler):
        self.session_handler = session_handler

    @property
    def session(self):
        return self.session_handler.session

    def create(self, user, data) -> Organization:
        organization = Organization(**data)
        organization.users.append(user)
        self.session.add(organization)

        try:
            self.session.commit()
            return organization
        except IntegrityError:
            raise ConflictError("organization")

    def get(self, id_: int) -> Organization:
        try:
            return self.session.query(Organization).filter_by(id=id_).one()
        except NoResultFound:
            raise NotFoundError("organization", id_)

    def list(self) -> List[Organization]:
        return self.session.query(Organization).all()

    def cast(self, d: dict) -> dict:
        return OrganizationSerializer().load(d)
