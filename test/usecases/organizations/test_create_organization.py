import pytest

from flasky.usecases.organizations import CreateOrganization
from flasky.services import OrganizationService
from flasky.exceptions import ValidationError, ConflictError
from flasky.models import User
from test import testutils
from test.factories import UserFactory


@pytest.fixture
def create_organization(session_handler) -> CreateOrganization:
    return CreateOrganization(OrganizationService(session_handler=session_handler))


VALID_ORGANIZATION_DATA = {"name": "My New Org"}


def test_create_organization(create_organization: CreateOrganization):
    user = UserFactory.create()
    org = create_organization.do(user, VALID_ORGANIZATION_DATA)

    assert org.id
    assert org.name == VALID_ORGANIZATION_DATA["name"]


def test_create_organization_with_long_username(
    create_organization: CreateOrganization
):
    user = UserFactory.create()
    long_name = str(["a"] * 100)
    data = {**VALID_ORGANIZATION_DATA, "name": long_name}

    testutils.assert_validation_errors(
        ["name"], lambda: create_organization.do(user, data)
    )


def test_cannot_create_organization_with_taken_name(
    create_organization: CreateOrganization
):
    user = UserFactory.create()
    create_organization.do(user, VALID_ORGANIZATION_DATA)

    with pytest.raises(ConflictError):
        create_organization.do(user, VALID_ORGANIZATION_DATA)


def test_organization_is_associated_with_user(
    create_organization: CreateOrganization, session
):
    user = UserFactory.create()
    organization = create_organization.do(user, VALID_ORGANIZATION_DATA)

    user = session.query(User).get(user.id)
    assert user.organization.id == organization.id
