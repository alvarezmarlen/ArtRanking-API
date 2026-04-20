from mongoengine import Document, StringField, ReferenceField, DateTimeField, IntField, ListField
from app.models.usuario import Usuario
from app.models.concurso import Concurso
from app.models.categoria import Categoria
from datetime import datetime


class Envio(Document):
    """
    Modelo de Envío (Submission).
    Representa una obra de arte subida por un usuario a un concurso.
    """
    # titulo: nombre de la obra
    # descripcion: descripción de la obra
    # imagen_url: URL de la imagen subida
    # autor: usuario que subió la obra
    # concurso: concurso al que participa
    # categoria: categoría dentro del concurso
    # votos: cantidad de votos recibidos
    # votantes: lista de usuarios que votaron (para evitar doble voto)
    # fecha_envio: cuando se subió
    titulo = StringField(required=True)
    descripcion = StringField()
    imagen_url = StringField(required=True)
    autor = ReferenceField(Usuario, required=True)
    concurso = ReferenceField(Concurso, required=True)
    categoria = ReferenceField(Categoria, required=True)
    votos = IntField(default=0)
    votantes = ListField(ReferenceField(Usuario))
    fecha_envio = DateTimeField(default=datetime.utcnow)

    meta = {
        "collection": "envios"  # nombre de la colección en MongoDB
    }
