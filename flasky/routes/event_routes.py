from flask import request, Flask

from flasky.serializers import EventSerializer
from flasky.routes.helpers import response
from flasky.usecases import Usecases


def make_event_routes(app: Flask, usecases: Usecases, d):
    @app.route("/events", methods=("POST",))
    @d.authed
    def create_event(user):
        event = usecases.create_event.do(user, request.json)
        return response({"event": EventSerializer().dump(event)}, 201)

    return app
