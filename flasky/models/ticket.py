import typing
from sqlalchemy import String, Column, Integer, ForeignKey, UniqueConstraint, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from . import Base
from .mixins import TimestampsMixin

if typing.TYPE_CHECKING:
    from .event import Event
    from .user import User


class Ticket(Base, TimestampsMixin):  # type: ignore
    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True)
    access_code = Column(
        UUID(), nullable=False, server_default=text("uuid_generate_v4()"), index=True
    )

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    user = relationship("User", back_populates="tickets")

    event_id = Column(Integer, ForeignKey("events.id"), nullable=False)
    event = relationship("Event", back_populates="tickets")

    __table_args__ = (UniqueConstraint("access_code"),)

    def __repr__(self):
        return "<Ticket id={} event_name={}>".format(self.id, self.event.name)
