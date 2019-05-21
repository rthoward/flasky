from flask import Flask

def make_routes(app: Flask):

    @app.route("/")
    def root():
        return "hello world"

