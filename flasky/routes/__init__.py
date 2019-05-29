from flask import Flask, request, Request, jsonify, make_response
import re
from functools import wraps

from flasky.services import UserService
from flasky.usecases import Usecases
from flasky import exceptions as e


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
    def root():
        return "hello world"

    @app.route("/users")
    def create_user():
        user = usecases.create_user.do("my username")
        return "create user"

    @app.route("/users/me")
    @authenticate
    def me(user=None):
        print(user)
        return "me"


def make_error_handlers(app):
    @app.errorhandler(e.AuthenticationError)
    def auth_error(e):
        json = jsonify({"error": {"status_code": 401, "message": "Unauthorized"}})
        return make_response(json, 401)

    @app.errorhandler(e.NotFoundError)
    def not_found_error(e):
        json = jsonify({"error": {"status_code": 404, "message": e.message}})
        return make_response(json, 401)
