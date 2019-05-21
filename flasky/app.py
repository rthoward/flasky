from flask import Flask
from flasky.routes import make_routes

def make_app():
    app = Flask(__name__)
    make_routes(app)

    return app


def make_config():
    return {}
