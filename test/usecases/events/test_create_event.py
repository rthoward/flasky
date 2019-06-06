import pytest
import pendulum

from flasky.usecases.events import CreateEvent
from flasky.services import EventService
from flasky.exceptions import ValidationError, ConflictError, MissingOrganizationError
from flasky.models import User, Organization
from test import testutils
from test.factories import UserFactory


@pytest.fixture
def create_event(session_handler) -> CreateEvent:
    return CreateEvent(EventService(session_handler=session_handler))


VALID_EVENT_DATA = {
    "name": "My New Event",
    "begins_at": pendulum.now().isoformat(),
    "ends_at": pendulum.now().add(hours=2).isoformat(),
    "capacity": 100,
}


def test_create_event(create_event: CreateEvent):
    user = UserFactory.create(with_org=True)
    event = create_event.do(user, VALID_EVENT_DATA)

    assert event.id
    assert event.name == VALID_EVENT_DATA["name"]


def test_user_must_have_org_to_create_event(create_event: CreateEvent):
    user = UserFactory.create()

    with pytest.raises(MissingOrganizationError):
        create_event.do(user, VALID_EVENT_DATA)


def test_org_cannot_have_two_events_with_same_name(create_event: CreateEvent):
    user = UserFactory.create(with_org=True)
    create_event.do(user, VALID_EVENT_DATA)

    with pytest.raises(ConflictError):
        create_event.do(user, VALID_EVENT_DATA)


def test_events_can_have_the_same_name_outside_of_org(create_event: CreateEvent):
    user1 = UserFactory.create(with_org=True)
    event1 = create_event.do(user1, VALID_EVENT_DATA)

    user2 = UserFactory.create(with_org=True)
    event2 = create_event.do(user2, VALID_EVENT_DATA)

    assert event1.name == event2.name


def test_event_is_associated_with_organization(create_event: CreateEvent, session):
    user = UserFactory.create(with_org=True)
    event = create_event.do(user, VALID_EVENT_DATA)

    org = session.query(Organization).get(user.organization_id)
    assert org.id == event.organization_id


def test_event_must_end_no_later_than_it_begins(create_event: CreateEvent):
    user = UserFactory.create(with_org=True)
    bad_data = {
        **VALID_EVENT_DATA,
        "begins_at": pendulum.now().isoformat(),
        "ends_at": pendulum.now().subtract(hours=1).isoformat(),
    }

    with pytest.raises(ValidationError):
        create_event.do(user, bad_data)
