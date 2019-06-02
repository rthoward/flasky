from marshmallow import fields, validate

from .base_schema import BaseSchema


class HoldRequestSerializer(BaseSchema):
    event_id = fields.Int()
    quantity = fields.Int()
