import datetime
from bson import ObjectId

from securemongoengine import EncryptedDecimalField, EncryptedStringField

from . import db, _key, _iv


class Income(db.EmbeddedDocument):
    _id = db.ObjectIdField(required=True, default=lambda: ObjectId())
    source = EncryptedStringField(key=str(_key), iv=str(_iv))
    amount = EncryptedDecimalField(key=str(_key), iv=str(_iv))
    frequency = EncryptedStringField(key=str(_key), iv=str(_iv))

    @property
    def dict(self):
        return {
            '_id': str(self._id),
            'source': self.source,
            'amount': str(self.amount),
            'frequency': self.frequency,
        }


class Ethnicity(db.EmbeddedDocument):
    ethnicity_name = EncryptedStringField(max_length=255, required=False, key=str(_key), iv=str(_iv))

    @property
    def dict(self):
        return self.ethnicity_name


class Person(db.EmbeddedDocument):
    _id = db.ObjectIdField(required=True, default=lambda: ObjectId())
    first_name = EncryptedStringField(max_length=255, required=False, key=str(_key), iv=str(_iv))
    middle_initial = EncryptedStringField(max_length=255, required=False, key=str(_key), iv=str(_iv))
    last_name = EncryptedStringField(max_length=255, required=False, key=str(_key), iv=str(_iv))
    incomes = db.EmbeddedDocumentListField(Income)
    ethnicities = db.EmbeddedDocumentListField(Ethnicity)
    meta = {
        'allow_inheritance': True,
    }

    @property
    def dict(self):
        return {
            '_id': str(self._id),
            'first_name': self.first_name,
            'middle_initial': self.middle_initial,
            'last_name': self.last_name,
            'incomes': [i.dict for i in self.incomes],
            'ethnicity': [e.dict for e in self.ethnicities]
        }


class Program(db.EmbeddedDocument):
    program_name = EncryptedStringField(max_length=255, required=False, key=str(_key), iv=str(_iv))

    @property
    def dict(self):
        return self.program_name


class Child(Person):
    school_zip = EncryptedStringField(max_length=15, required=False, key=str(_key), iv=str(_iv))
    school_city = EncryptedStringField(max_length=255, required=False, key=str(_key), iv=str(_iv))
    school_state = EncryptedStringField(max_length=255, required=False, key=str(_key), iv=str(_iv))
    school_name = EncryptedStringField(max_length=255, required=False, key=str(_key), iv=str(_iv))
    programs = db.EmbeddedDocumentListField(Program)

    @property
    def dict(self):
        return {
            '_id': str(self._id),
            'first_name': self.first_name,
            'middle_initial': self.middle_initial,
            'last_name': self.last_name,
            'school_zip': self.school_zip,
            'school_city': self.school_city,
            'school_state': self.school_state,
            'school_name': self.school_name,
            'incomes': [i.dict for i in self.incomes],
            'programs': [p.dict for p in self.programs],
            'ethnicities': [e.dict for e in self.ethnicities]
        }


class Signature(db.EmbeddedDocument):
    _id = db.ObjectIdField(required=True, default=lambda: ObjectId())
    name = EncryptedStringField(max_length=255, required=True, key=str(_key), iv=str(_iv))
    date = db.DateTimeField(default=datetime.datetime.utcnow(), required=True)
    ip_address = EncryptedStringField(max_length=255, required=True, key=str(_key), iv=str(_iv))
    attestation = db.StringField(required=True)

    @property
    def dict(self):
        return {
            '_id': str(self._id),
            'name': self.name,
            'date': self.date,
            'ip_address': self.ip_address,
            'attestation': self.attestation,
        }


class Applicant(Person):
    _id = db.ObjectIdField(required=True, default=lambda: ObjectId())
    ssn = EncryptedStringField(min_length=4, max_length=4, required=False, key=str(_key), iv=str(_iv))
    address_1 = EncryptedStringField(max_length=255, required=False, key=str(_key), iv=str(_iv))
    address_2 = EncryptedStringField(max_length=255, required=False, key=str(_key), iv=str(_iv))
    postal = EncryptedStringField(max_length=32, required=False, key=str(_key), iv=str(_iv))
    city = EncryptedStringField(max_length=255, required=False, key=str(_key), iv=str(_iv))
    state = EncryptedStringField(max_length=255, required=False, key=str(_key), iv=str(_iv))

    @property
    def dict(self):
        return {
            '_id': str(self._id),
            'first_name': self.first_name,
            'middle_initial': self.middle_initial,
            'last_name': self.last_name,
            'incomes': [i.dict for i in self.incomes],
            'ssn': self.ssn,
            'address_1': self.address_1,
            'address_2': self.address_2,
            'postal': self.postal,
            'city': self.city,
            'state': self.state
        }


class Application(db.Document):
    created_at = db.DateTimeField(default=datetime.datetime.utcnow(), required=True)
    email = db.EmailField(unique=False, required=False)

    applicant = db.EmbeddedDocumentField(Applicant)
    children = db.EmbeddedDocumentListField(Child)
    persons = db.EmbeddedDocumentListField(Person)
    signature = db.EmbeddedDocumentField(Signature)

    def __str__(self):
        return '{} ({})'.format(str(self.id), self.email)

    meta = {
        'allow_inheritance': True,
        'indexes': ['-created_at', 'email'],
        'ordering': ['-created_at']
    }

    @property
    def dict(self):
        return {
            '_id': str(self.id),
            'created_at': str(self.created_at),
            'applicant': self.applicant.dict if self.applicant else None,
            'children': [c.dict for c in self.children] if self.children else [],
            'persons': [p.dict for p in self.persons] if self.persons else [],
            'signature': self.signature.dict if self.signature else None
        }
