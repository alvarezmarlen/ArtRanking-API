from mongoengine import Document, StringField, DateTimeField, ReferenceField
import datetime

class Comentario(Document):
    usuario = ReferenceField('Usuario', required=True)
    envio = ReferenceField('Envio', required=True)
    texto = StringField(required=True)
    fecha = DateTimeField(default=datetime.datetime.utcnow)