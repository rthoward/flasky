from sqlalchemy import String, Column, Integer
from sqlalchemy.orm import relationship

from . import Base


class Organization(Base):  # type: ignore
    __tablename__ = "organizations"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)

    users = relationship("User")

    def __repr__(self):
        return "<Organization id={} name={}>".format(self.id, self.name)
