from sqlalchemy.orm import sessionmaker
import pendulum

import sys
from unipath import Path

parent_dir = Path(__file__).parent.parent
sys.path.append(parent_dir)

from flasky.models import User, Organization, Event, Ticket
from flasky.app import make_config, make_engine

session = sessionmaker(bind=make_engine(make_config()))()


alex = User(username="alex")
belinda = User(username="belinda")

org = Organization(users=[alex], name="Burrito Town")
event = Event(
    organization=org,
    name="Burrito Madness",
    capacity=50,
    begins_at=pendulum.now(),
    ends_at=pendulum.now().add(weeks=1),
)
tickets = [Ticket(user=belinda, event=event) for _ in range(3)]

session.add_all([alex, belinda, org, event] + tickets)
session.commit()
