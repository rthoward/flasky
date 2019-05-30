from marshmallow import Schema, fields


class UserSerializer(Schema):
    id = fields.Int()
    username = fields.String()
