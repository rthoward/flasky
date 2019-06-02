from sqlalchemy.orm import sessionmaker
from flasky.app import make_config, make_engine

from flasky.models import *
from test.factories import *

session = sessionmaker(bind=make_engine(make_config()))()

print(
    "\nWelcome to Flasky. This shell has all models in scope, and a SQLAlchemy session called session."
)
