from mongoengine import Document, StringField, ReferenceField
from app.models.concurso import Concurso


class Categoria(Document):
    """
    Modelo de Categoría.
    Clasifica los envíos dentro de un concurso (ej: pintura, escultura, digital).
    """
    # nombre: identificador de la categoría
    # descripcion: detalles de qué incluye
    # concurso: a qué concurso pertenece
    nombre = StringField(required=True)
    descripcion = StringField()
    concurso = ReferenceField(Concurso, required=True)

    meta = {
        "collection": "categorias"  # nombre de la colección en MongoDB
    }
