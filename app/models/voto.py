from mongoengine import Document, StringField, IntField

class Voto(Document):
    user_id = StringField(required=True)
    submission_id = StringField(required=True)
    value = IntField(default=1)