import factory
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
