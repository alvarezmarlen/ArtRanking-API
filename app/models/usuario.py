from mongoengine import Document, StringField, EmailField

class Usuario(Document):
    email = EmailField(required=True, unique=True)
    password = StringField(required=True)
    role = StringField(default="user")