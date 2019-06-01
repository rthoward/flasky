import factory
from flasky import models


class UserFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = models.User

    username = factory.Faker("first_name")
