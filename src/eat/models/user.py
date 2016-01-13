import datetime

from argon2 import PasswordHasher

from . import db


class User(db.Document):
    created_at = db.DateTimeField(default=datetime.datetime.utcnow(), required=True)
    email = db.EmailField(unique=True, required=True)
    email_verified_at = db.DateTimeField(default=None, required=False)
    password_hash = db.StringField(max_length=255, required=True)

    first_name = db.StringField(max_length=255, required=False)
    middle_initial = db.StringField(max_length=255, required=False)
    last_name = db.StringField(max_length=255, required=False)

    @property
    def password(self):
        return self.password_hash

    @password.setter
    def password(self, password):
        hasher = PasswordHasher()
        ph = hasher.hash(password)
        self.password_hash = ph

    def verify_password(self, password):
        hasher = PasswordHasher()
        return hasher.verify(self.password_hash, password)

    def __unicode__(self):
        return self.email

    meta = {
        'allow_inheritance': True,
        'indexes': ['-created_at', 'email'],
        'ordering': ['-created_at']
    }
