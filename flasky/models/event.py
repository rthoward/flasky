from sqlalchemy import (
    String,
    Column,
    Integer,
    ForeignKey,
    UniqueConstraint,
    TIMESTAMP,
    CheckConstraint,
)
from sqlalchemy.orm import relationship

from . import Base
from .mixins import TimestampsMixin


class Event(Base, TimestampsMixin):  # type: ignore
    __tablename__ = "events"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    organization_id = Column(Integer, ForeignKey("organizations.id"), nullable=False)
    organization = relationship("Organization", back_populates="events")

    begins_at = Column(TIMESTAMP(timezone=True), nullable=False)
    ends_at = Column(TIMESTAMP(timezone=True), nullable=False)

    __table_args__ = (
        UniqueConstraint("organization_id", "name"),
        CheckConstraint("begins_at <= ends_at", name="check_times"),
    )

    def __repr__(self):
        return "<Event id={} name={}>".format(self.id, self.name)
