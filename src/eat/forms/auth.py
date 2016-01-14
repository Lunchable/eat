from flask import request
from flask_wtf import Form
from wtforms import StringField, PasswordField, HiddenField
from wtforms.validators import InputRequired, Email, ValidationError
from wtforms.widgets import PasswordInput

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


class SignIn(Form):
    email = StringField('Email', [InputRequired(message=u'Email is required'),
                                  Email(message=u'Invalid email address.'),
                                  EmailExists()])
    password = PasswordField('Password',
                             [InputRequired(message=u'Password is required')],
                             widget=PasswordInput(hide_value=False))
    redir_url = HiddenField(default=lambda: request.full_path)

    def validate_password(self, field):
        """
        TODO: Prevent login bomb
        """
        user = self.get_user()
        if not user.verify_password(self.password.data):
            raise ValidationError('Incorrect Password')

    def get_user(self):
        return User.objects(email=self.email.data).first()

# class SignUp(Form):
#     first_name = StringField('First Name',
#                            [InputRequired(message=u'First name is required')])
#     last_name = StringField('Last Name',
#                           [InputRequired(message=u'Last name is required')])
#     location = StringField(label='City of Primary Residence',
#                          description='City, State, Country',
#                          validators=[])
#     email = StringField('Email Address',
#                       [InputRequired(message=u'Email is required'),
#                        Email(message=u'Invalid email address.'),
#                        EmailExists(should_exist=False)])
#
#     password = PasswordField(
#             'Create Password',
#             [InputRequired(message=u'Password is required'),
#              Length(min=8, message=u'Password must be at least 8 characters long')],
#             widget=PasswordInput(hide_value=False))
#     agree = BooleanField(
#             '',
#             [InputRequired(
#                     message=u'You must agree to the Terms of Use to create an account')])
#     subscribe = BooleanField('')
#     redir_url = HiddenField(default=lambda: request.full_path)
#
#     def get_user(self):
#         return SiteUser.query.filter(SiteUser.email == self.email.data).first()
