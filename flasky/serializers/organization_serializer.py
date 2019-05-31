from marshmallow import fields, validate

from .base_schema import BaseSchema


class OrganizationSerializer(BaseSchema):
    id = fields.Int()
    name = fields.String(required=True, validate=[validate.Length(max=50)])
