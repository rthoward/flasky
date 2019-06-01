from flask import request, Flask

from flasky.serializers import OrganizationSerializer
from flasky.routes.helpers import response
from flasky.usecases import Usecases


def make_organization_routes(app: Flask, usecases: Usecases, d):
    @app.route("/organizations", methods=("POST",))
    @d.authed
    def create_organization(user):
        organization = usecases.create_organization.do(user, request.json)
        return response(
            {"organization": OrganizationSerializer().dump(organization)}, 201
        )

    return app
