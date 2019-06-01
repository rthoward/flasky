from sqlalchemy import String, Column, Integer, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship

from . import Base
from .mixins import TimestampsMixin


class Event(Base, TimestampsMixin):  # type: ignore
    __tablename__ = "events"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    organization_id = Column(Integer, ForeignKey("organizations.id"), nullable=False)
    organization = relationship("Organization", back_populates="events")

    __table_args__ = (UniqueConstraint("organization_id", "name"),)

    def __repr__(self):
        return "<Event id={} name={}>".format(self.id, self.name)
