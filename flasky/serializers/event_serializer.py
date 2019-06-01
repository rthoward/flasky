from marshmallow import fields, validate

from .base_schema import BaseSchema


class EventSerializer(BaseSchema):
    id = fields.Int(dump_only=True)
    name = fields.String(required=True, validate=[validate.Length(max=50)])
    organization_id = fields.Int(dump_only=True)
