from flask import request

from flasky.serializers import UserSerializer
from flasky.routes.helpers import response


def make_user_routes(app, usecases, d):
    @app.route("/users", methods=("POST",))
    def create_user():
        user = usecases.create_user.do(request.json)
        return response({"user": UserSerializer().dump(user)}, 201)

    @app.route("/users/me")
    @d.authed
    def me(user):
        return response({"user": UserSerializer().dump(user)})

    return app
