from flask.ext.mongoengine import MongoEngine
from flask import current_app
from werkzeug.local import LocalProxy
from securemongoengine.fields import EncryptedField

db = MongoEngine()

_algorithm = EncryptedField._AES
_key = LocalProxy(lambda: current_app.config.get('SECRET_KEY'))
_iv = LocalProxy(lambda: current_app.config.get('IV'))
