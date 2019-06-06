from marshmallow import fields, validate, validates_schema, ValidationError

from .base_schema import BaseSchema


class EventSerializer(BaseSchema):
    id = fields.Int(dump_only=True)
    name = fields.String(required=True, validate=[validate.Length(max=50)])
    organization_id = fields.Int(dump_only=True)
    capacity = fields.Int()
    begins_at = fields.DateTime()
    ends_at = fields.DateTime()

    @validates_schema
    def validate_timestamps(self, data):
        if data["begins_at"] > data["ends_at"]:
            raise ValidationError("Event cannot end before it begins.")
