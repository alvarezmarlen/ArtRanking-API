from marshmallow import Schema, fields, validate

class UsuarioSchema(Schema):
    """esquema para validar el registro de un usuario."""
    email = fields.Email(required=True, error_messages={
        "required": "El email es obligatorio",
        "invalid": "El formato del email es inválido"
    })
    password = fields.String(required=True, validate=validate.Length(min=6), error_messages={
        "required": "La contraseña es obligatoria",
        "min": "La contraseña debe tener al menos 6 caracteres"
    })