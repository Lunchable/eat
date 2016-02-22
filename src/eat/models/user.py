import datetime

from argon2 import PasswordHasher

from . import db
from application import Application
import mongoengine


class User(db.Document):
    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)

    created_at = db.DateTimeField(default=datetime.datetime.utcnow(), required=True)
    email = db.EmailField(unique=True, required=True)
    email_verified_at = db.DateTimeField(default=None, required=False)
    password_hash = db.StringField(max_length=255, required=True)

    first_name = db.StringField(max_length=255, required=False)
    middle_initial = db.StringField(max_length=255, required=False)
    last_name = db.StringField(max_length=255, required=False)

    applications = db.ListField(db.ReferenceField(Application), reverse_delete_rule=mongoengine.PULL)

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
        try:
            hasher.verify(self.password_hash, password)
            return True
        except Exception:
            return False

    def __unicode__(self):
        return self.email

    meta = {
        'allow_inheritance': True,
        'indexes': ['-created_at', 'email'],
        'ordering': ['-created_at']
    }
