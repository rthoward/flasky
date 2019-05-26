import factory
from flasky import models


class UserFactory(factory.Factory):
    class Meta:
        model = models.User
