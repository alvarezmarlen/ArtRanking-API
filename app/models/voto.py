from mongoengine import Document, ReferenceField, IntField

class Voto(Document):
    usuario = ReferenceField('Usuario', required=True)
    envio = ReferenceField('Envio', required=True)
    value = IntField(default=1)