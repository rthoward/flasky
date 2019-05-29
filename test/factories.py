from factory.alchemy import SQLAlchemyModelFactory
from flasky import models


class UserFactory(SQLAlchemyModelFactory):
    class Meta:
        model = models.User
