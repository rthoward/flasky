class AuthenticationError(Exception):
    pass


class NotFoundError(Exception):
    def __init__(self, resource, id_=None):
        message = "{} not found".format(resource)
        if id_ is not None:
            message += " with id {}".format(id_)

        super().__init__(message)
        self.message = message
        self.resource = resource
        self.id = id_
