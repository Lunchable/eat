import datetime
from . import db
from securemongoengine import EncryptedDecimalField, EncryptedStringField



class Application(db.Document):
    created_at = db.DateTimeField(default=datetime.datetime.utcnow(), required=True)
    email = db.EmailField(unique=False, required=True)

    applicant = db.EmbeddedDocumentField(Applicant)
    children = db.ListField(db.EmbeddedDocumentField(Child))
    household = db.ListField(db.EmbeddedDocumentField(Person))
    signature = db.EmbeddedDocumentField(Signature)

    def __unicode__(self):
        return '{} ({})'.format(unicode(self.id), self.email)

    meta = {
        'allow_inheritance': True,
        'indexes': ['-created_at', 'email'],
        'ordering': ['-created_at']
    }


class Person(db.Document):
    first_name = EncryptedStringField(max_length=255, required=False)
    middle_initial = EncryptedStringField(max_length=255, required=False)
    last_name = EncryptedStringField(max_length=255, required=False)


class Applicant(Person):
    ssn = EncryptedStringField(min_length=4, max_length=4, required=False)
    postal = EncryptedStringField(max_length=32, required=False)
    city = EncryptedStringField(max_length=255, required=False)
    state = EncryptedStringField(max_length=255, required=False)


class Child(Person):
    pass


class Signature(db.Document):
    name = EncryptedStringField(max_length=255, required=True)
    date = db.DateTimeField(default=datetime.datetime.utcnow(), required=True)
    ip_address = EncryptedStringField(max_length=255, required=True)
    attestation = db.StringField(required=True)
