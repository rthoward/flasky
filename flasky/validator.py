from cerberus import Validator as CerberusValidator # type: ignore


class ValidationError(Exception):
    def __init__(self, errors):
        self.errors = errors


class Validator(CerberusValidator):
    def validate(self, *args, **kwargs):
        result = super().validate(*args, **kwargs)
        if not result:
            raise ValidationError(self.errors)