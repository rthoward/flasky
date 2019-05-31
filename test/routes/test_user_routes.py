from test.factories import UserFactory
from flask import url_for
from flasky.models import User


def test_me_returns_401_if_not_authed(client, session):
    response = client.get(url_for("me"))
    assert response.status_code == 401


def test_me_returns_user_when_successful(client, session):
    user = UserFactory.create(username="meow")
    headers = {"Authorization": "Bearer {}".format(user.id)}

    response = client.get(url_for("me"), headers=headers)

    assert response.status_code == 200

    assert response.json["user"]["id"] == user.id
    assert response.json["user"]["username"] == "meow"
