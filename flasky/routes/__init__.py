from flask import Flask, request, Request, jsonify, make_response
import re
from functools import wraps

from flasky.services import UserService
from flasky.usecases import Usecases
from flasky import exceptions as e
from flasky.models import User
from flasky.serializers import UserSerializer


def make_routes(app: Flask, usecases: Usecases):

    make_error_handlers(app)

    def authenticate(f, required=True):
        @wraps(f)
        def wrapper(*args, **kwargs):
            user = usecases.auth.do(request, required)
            kwargs_ = {**kwargs, "user": user}
            return f(*args, **kwargs_)

        return wrapper

    @app.route("/")
    def health():
        return jsonify({"status": "ok"})

    @app.route("/users", methods=("POST",))
    def create_user():
        user = usecases.create_user.do(request.json)
        return jsonify({"user": UserSerializer().dump(user)})

    @app.route("/users/me")
    @authenticate
    def me(user):
        return jsonify({"user": UserSerializer().dump(user)})

    return app


def make_error_handlers(app):
    @app.errorhandler(e.AuthenticationError)
    def auth_error(e):
        json = jsonify({"error": {"status_code": 401, "message": "Unauthorized"}})
        return make_response(json, 401)

    @app.errorhandler(e.NotFoundError)
    def not_found_error(e):
        json = jsonify({"error": {"status_code": 404, "message": e.message}})
        return make_response(json, 401)

    @app.errorhandler(e.ValidationError)
    def validation_error(e):
        json = jsonify(
            {
                "error": {
                    "status_code": 400,
                    "message": "validation-error",
                    "details": e.field_errors,
                }
            }
        )
        return make_response(json, 400)
