import pytest
import pendulum

from flasky.usecases.holds import CreateHold
from flasky.services import HoldService, TicketService
from test.factories import UserFactory, EventFactory


@pytest.fixture
def create_hold(session_handler) -> CreateHold:
    return CreateHold(
        hold_service=HoldService(session_handler=session_handler),
        ticket_service=TicketService(session_handler),
    )


def test_create_hold(create_hold: CreateHold):
    user = UserFactory.create()
    event = EventFactory.create()

    hold = create_hold.do(user, {"event_id": event.id, "quantity": 3})
