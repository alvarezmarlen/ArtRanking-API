from mongoengine import Document, StringField, DateTimeField, ReferenceField, ListField, BooleanField
from app.models.usuario import Usuario
from datetime import datetime


class Concurso(Document):
    """
    Modelo de Concurso.
    Representa un evento artístico donde usuarios pueden enviar obras.
    """
    # titulo: nombre del concurso
    # descripcion: detalles del concurso
    # fecha_inicio: cuando empieza
    # fecha_fin: cuando termina
    # estado: activo, cerrado, cancelado
    # creado_por: usuario admin que lo creó
    # categorias: lista de categorías del concurso
    # activo: si está visible o eliminado
    titulo = StringField(required=True)
    descripcion = StringField()
    fecha_inicio = DateTimeField(required=True)
    fecha_fin = DateTimeField(required=True)
    estado = StringField(default="activo")
    creado_por = ReferenceField(Usuario, required=True)
    categorias = ListField(ReferenceField("Categoria"))
    activo = BooleanField(default=True)
    fecha_creacion = DateTimeField(default=datetime.utcnow)

    meta = {
        "collection": "concursos"  # nombre de la colección en MongoDB
    }
