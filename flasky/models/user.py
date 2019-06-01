import typing
from sqlalchemy import String, Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from . import Base
from .mixins import TimestampsMixin

if typing.TYPE_CHECKING:
    from .organization import Organization


class User(Base, TimestampsMixin):  # type: ignore
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False)

    organization_id = Column(Integer, ForeignKey("organizations.id"), nullable=True)
    organization = relationship("Organization", back_populates="users")

    def __repr__(self):
        return "<User id={}>".format(self.id)

    @property
    def in_organization(self):
        return self.organization_id is not None
