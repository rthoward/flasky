from flask import request
from functools import wraps


class Decorators(object):
    def __init__(self, usecases):
        self.usecases = usecases

    def authed(self, f, required=True):
        @wraps(f)
        def wrapper(*args, **kwargs):
            user = self.usecases.auth.do(request, required)
            kwargs_ = {**kwargs, "user": user}
            return f(*args, **kwargs_)

        return wrapper
