from sqlalchemy import String, Column, Integer

from . import Base


class User(Base):  # type: ignore
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False)

    def __repr__(self):
        return "<User id={}>".format(self.id)
