import factory
import pendulum
import random

from flasky import models


class UserFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = models.User

    username = factory.Faker("first_name")
    organization = None

    @classmethod
    def _adjust_kwargs(cls, **kwargs):
        if kwargs.pop("with_org", False):
            kwargs["organization"] = OrganizationFactory.build()

        return kwargs


class OrganizationFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = models.Organization

    name = factory.LazyFunction(
        lambda: "{} Organization".format(factory.Faker("domain_word"))
    )


class EventFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = models.Event

    name = factory.LazyFunction(
        lambda: "{} Event #{}".format(factory.Faker("domain_word"), random.randrange(1))
    )
    begins_at = pendulum.datetime(2020, 1, 2, 3)
    ends_at = pendulum.datetime(2020, 1, 3, 3)
    organization = factory.SubFactory(OrganizationFactory)
    capacity = 100


class HoldFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = models.Hold
