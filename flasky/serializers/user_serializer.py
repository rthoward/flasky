from marshmallow import fields, validate

from .base_schema import BaseSchema


class UserSerializer(BaseSchema):
    id = fields.Int()
    username = fields.String(required=True, validate=[validate.Length(max=50)])
