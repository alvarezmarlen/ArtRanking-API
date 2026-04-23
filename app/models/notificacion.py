from mongoengine import Document, StringField, BooleanField, DateTimeField
import datetime

class Notificacion(Document):
    user_id = StringField(required=True)
    tipo = StringField()  # voto, comentario
    mensaje = StringField()
    leido = BooleanField(default=False)
    fecha = DateTimeField(default=datetime.datetime.utcnow)