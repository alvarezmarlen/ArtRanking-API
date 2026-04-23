from mongoengine import Document, StringField


class Categoria(Document):
    """
    Modelo de Categoría.
    Clasifica los envíos (ej: pintura, escultura, digital).
    Catálogo maestro independiente de concursos.
    """
    # nombre: identificador de la categoría
    # descripcion: detalles de qué incluye
    nombre = StringField(required=True)
    descripcion = StringField()

    meta = {
        "collection": "categorias"  # nombre de la colección en MongoDB
    }
