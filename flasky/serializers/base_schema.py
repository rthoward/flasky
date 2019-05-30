import marshmallow
from flasky.exceptions import ValidationError


class BaseSchema(marshmallow.Schema):
    def load(self, *args, **kwargs):
        try:
            return super().load(*args, **kwargs)
        except marshmallow.exceptions.ValidationError as e:
            raise ValidationError(e.messages)
