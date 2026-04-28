from marshmallow import Schema, fields

class VotoSchema(Schema):
    submission_id = fields.String(required=True)