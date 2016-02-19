from wtforms.validators import InputRequired, Email, ValidationError
from eat.models.user import User


class EmailExists(object):
    def __init__(self, should_exist=True, message=None):
        self._email_should_exist = should_exist
        self._message = message

    def __call__(self, form, field):
        exists = User.objects(email=field.data).first()
        if self._email_should_exist and not exists:
            raise ValidationError(self._message or u'Email not found.')

        if not self._email_should_exist and exists:
            raise ValidationError(self._message or u'Email exists.')
