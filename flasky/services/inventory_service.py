from sqlalchemy import func

from flasky.models import Event, Ticket, Hold


class Inventory(object):
    def __init__(self, event, total, available, held, purchased):
        self.event = event
        self.total = total
        self.available = available
        self.held = held
        self.purchased = purchased


class InventoryService(object):
    def __init__(self, session_handler):
        self.session_handler = session_handler

    @property
    def session(self):
        return self.session_handler.session

    def for_event(self, event: Event) -> Inventory:
        num_held = (
            self.session.query(func.sum(Hold.quantity))
            .filter(Hold.event == event)
            .scalar()
        )
        num_purchased = (
            self.session.query(func.count(Ticket.id))
            .filter(Ticket.event == event)
            .scalar()
        )
        num_available = event.capacity - (num_held + num_purchased)
        return Inventory(
            event=event,
            total=event.capacity,
            available=num_available,
            held=num_held,
            purchased=num_purchased,
        )
