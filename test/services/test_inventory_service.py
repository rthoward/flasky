import pytest

from flasky.services import InventoryService
from test.factories import EventFactory, HoldFactory, UserFactory


@pytest.fixture
def inventory_service(session_handler):
    return InventoryService(session_handler=session_handler)


def test_purchased_inventory(inventory_service: InventoryService):
    user = UserFactory.create()
    event = EventFactory.create(capacity=100)
    HoldFactory.create(user=user, event=event, quantity=3)

    inventory = inventory_service.for_event(event)

    assert inventory.available == 97
    assert inventory.event == event
    assert inventory.total == 100
