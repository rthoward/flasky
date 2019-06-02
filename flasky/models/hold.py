import typing
from sqlalchemy import String, Column, Integer, ForeignKey, UniqueConstraint, TIMESTAMP
from sqlalchemy.orm import relationship

from . import Base
from .mixins import TimestampsMixin

if typing.TYPE_CHECKING:
    from .event import Event
    from .user import User


class Hold(Base, TimestampsMixin):  # type: ignore
    __tablename__ = "holds"

    id = Column(Integer, primary_key=True)
    quantity = Column(Integer, nullable=False)
    ends_at = Column(TIMESTAMP(timezone=False), nullable=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    user = relationship("User", back_populates="holds")

    event_id = Column(Integer, ForeignKey("events.id"), nullable=False, index=True)
    event = relationship("Event", back_populates="holds")

    __table_args__ = (UniqueConstraint("user_id", "event_id"),)

    def __repr__(self):
        return "<Hold id={} event_name={} qty={}>".format(
            self.id, self.event.name, self.quantity
        )
