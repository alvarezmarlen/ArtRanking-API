"""
Esquemas de validación para Envíos y Concursos (Marshmallow).
Validan datos de entrada en los endpoints.
"""
from marshmallow import Schema, fields, validate


class EnvioCreateSchema(Schema):
    """Valida datos al crear un envío."""
    titulo = fields.String(required=True, validate=validate.Length(min=3, max=100))
    descripcion = fields.String()
    imagen_url = fields.Url(required=True)
    concurso_id = fields.String(required=True)
    categoria_id = fields.String(required=True)
    etiquetas = fields.List(fields.String())


class EnvioUpdateSchema(Schema):
    """Valida datos al actualizar un envío (todos opcionales)."""
    titulo = fields.String(validate=validate.Length(min=3, max=100))
    descripcion = fields.String()
    imagen_url = fields.Url()


class CategoriaSchema(Schema):
    """Valida datos de una categoría."""
    nombre = fields.String(required=True)
    descripcion = fields.String()


class ConcursoCreateSchema(Schema):
    """Valida datos al crear un concurso con categorías opcionales."""
    titulo = fields.String(required=True, validate=validate.Length(min=3, max=100))
    descripcion = fields.String()
    fecha_inicio = fields.DateTime(required=True)
    fecha_fin = fields.DateTime(required=True)
    categorias = fields.List(fields.Nested(CategoriaSchema))


class VotoSchema(Schema):
    """Valida datos de un voto."""
    envio_id = fields.String(required=True)
