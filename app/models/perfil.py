from mongoengine import Document, StringField, ReferenceField
from app.models.usuario import Usuario

class Perfil(Document):
    usuario = ReferenceField(Usuario, required=True)
    nombre = StringField()
    avatar = StringField()
    bio = StringField()