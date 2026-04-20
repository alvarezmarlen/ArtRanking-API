from mongoengine import Document, StringField


class Etiqueta(Document):
    """
    Modelo de Etiqueta (Tag).
    Palabras clave para organizar y buscar envíos.
    Ejemplos: "retrato", "paisaje", "abstracto", "3D"
    """
    # nombre: texto de la etiqueta (único)
    nombre = StringField(required=True, unique=True)

    meta = {
        "collection": "etiquetas"  # nombre de la colección en MongoDB
    }
