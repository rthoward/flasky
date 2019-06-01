from test.factories import UserFactory
from flask import url_for
from flasky.models import User


def test_create_organization_returns_401_if_not_authed(client, session):
    response = client.post(url_for("create_organization"))
    assert response.status_code == 401


def test_create_organization_returns_organization_when_successful(client, session):
    user = UserFactory.create(username="meow")
    headers = {"Authorization": "Bearer {}".format(user.id)}

    org_data = {"name": "My Organization"}

    response = client.post(
        url_for("create_organization"), headers=headers, json=org_data
    )

    assert response.status_code == 201

    assert response.json["organization"]["id"]
    assert response.json["organization"]["name"] == "My Organization"
