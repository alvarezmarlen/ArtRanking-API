from marshmallow import Schema, fields

class UsuarioSchema(Schema):
    email = fields.Email(required=True)
    password = fields.String(required=True)