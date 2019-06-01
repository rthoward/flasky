from flask import Flask, request, Request, jsonify, make_response
import re
from functools import wraps

from flasky.services import UserService
from flasky.usecases import Usecases
from flasky import exceptions as e
from flasky.models import User
from flasky.serializers import UserSerializer

from .user_routes import make_user_routes
from .organization_routes import make_organization_routes
from .decorators import Decorators


def make_routes(app: Flask, usecases: Usecases):

    make_error_handlers(app)
    decorators = Decorators(usecases)
    app = make_user_routes(app, usecases, decorators)
    app = make_organization_routes(app, usecases, decorators)

    @app.route("/")
    def health():
        return jsonify({"status": "ok"})

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
