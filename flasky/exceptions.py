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


class ValidationError(Exception):
    def __init__(self, field_errors):
        message = str(field_errors)

        super().__init__(message)
        self.message = message
        self.field_errors = field_errors


class ConflictError(Exception):
    def __init__(self, resource):
        message = "{} with that data already exists".format(resource)
        super().__init__(message)
        self.resource = resource
