from flask import Flask


def make_routes(app: Flask, usecases):
    @app.route("/")
    def root():
        return "hello world"

    @app.route("/users")
    def create_user():
        user = usecases.create_user.do("my username")
        return "create user"
