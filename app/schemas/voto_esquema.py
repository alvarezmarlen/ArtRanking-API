from marshmallow import Schema, fields

class VotoSchema(Schema):
    user_id = fields.String(required=True)
    submission_id = fields.String(required=True)