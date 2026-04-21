from mongoengine import Document, StringField, DateTimeField
import datetime

class Comentario(Document):
    user_id = StringField(required=True)
    submission_id = StringField(required=True)
    texto = StringField(required=True)
    fecha = DateTimeField(default=datetime.datetime.utcnow)