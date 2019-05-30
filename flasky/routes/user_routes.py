from flask import request, jsonify

from flasky.serializers import UserSerializer


def make_user_routes(app, usecases, d):
    @app.route("/users", methods=("POST",))
    def create_user():
        user = usecases.create_user.do(request.json)
        return jsonify({"user": UserSerializer().dump(user)})

    @app.route("/users/me")
    @d.authenticate
    def me(user):
        return jsonify({"user": UserSerializer().dump(user)})

    return app
