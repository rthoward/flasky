from flasky.app import make_config, make_flask_app, make_routes

config = make_config()
app = make_flask_app(config)
make_routes(app)
