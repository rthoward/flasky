from sqlalchemy import String, Column, Integer
from sqlalchemy.orm import relationship

from . import Base
from .mixins import TimestampsMixin


class Organization(Base, TimestampsMixin):  # type: ignore
    __tablename__ = "organizations"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)

    users = relationship("User")
    events = relationship("Event")

    def __repr__(self):
        return "<Organization id={} name={}>".format(self.id, self.name)
