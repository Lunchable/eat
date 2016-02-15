import datetime
from bson import ObjectId

from securemongoengine import EncryptedDecimalField, EncryptedStringField

from . import db, _key, _iv


class Income(db.EmbeddedDocument):
    _id = db.ObjectIdField(required=True, default=lambda: ObjectId())
    source = EncryptedStringField(key=str(_key), iv=str(_iv))
    amount = EncryptedDecimalField(key=str(_key), iv=str(_iv))
    frequency = EncryptedStringField(key=str(_key), iv=str(_iv))


class Person(db.EmbeddedDocument):
    _id = db.ObjectIdField(required=True, default=lambda: ObjectId())
    first_name = EncryptedStringField(max_length=255, required=False, key=str(_key), iv=str(_iv))
    middle_initial = EncryptedStringField(max_length=255, required=False, key=str(_key), iv=str(_iv))
    last_name = EncryptedStringField(max_length=255, required=False, key=str(_key), iv=str(_iv))
    incomes = db.EmbeddedDocumentListField(Income)
    meta = {
        'allow_inheritance': True,
    }


class Child(Person):
    pass


class Signature(db.EmbeddedDocument):
    _id = db.ObjectIdField(required=True, default=lambda: ObjectId())
    name = EncryptedStringField(max_length=255, required=True, key=str(_key), iv=str(_iv))
    date = db.DateTimeField(default=datetime.datetime.utcnow(), required=True)
    ip_address = EncryptedStringField(max_length=255, required=True, key=str(_key), iv=str(_iv))
    attestation = db.StringField(required=True)


class Applicant(Person):
    _id = db.ObjectIdField(required=True, default=lambda: ObjectId())
    ssn = EncryptedStringField(min_length=4, max_length=4, required=False, key=str(_key), iv=str(_iv))
    postal = EncryptedStringField(max_length=32, required=False, key=str(_key), iv=str(_iv))
    city = EncryptedStringField(max_length=255, required=False, key=str(_key), iv=str(_iv))
    state = EncryptedStringField(max_length=255, required=False, key=str(_key), iv=str(_iv))


class Application(db.Document):
    created_at = db.DateTimeField(default=datetime.datetime.utcnow(), required=True)
    email = db.EmailField(unique=False, required=True)

    applicant = db.EmbeddedDocumentField(Applicant)
    children = db.EmbeddedDocumentListField(Child)
    household = db.EmbeddedDocumentListField(Person)
    signature = db.EmbeddedDocumentField(Signature)

    def __str__(self):
        return '{} ({})'.format(str(self.id), self.email)

    meta = {
        'allow_inheritance': True,
        'indexes': ['-created_at', 'email'],
        'ordering': ['-created_at']
    }
