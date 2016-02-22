from flask import request
from flask_wtf import Form
from wtforms import StringField, PasswordField, HiddenField
from wtforms.validators import InputRequired, Email, ValidationError
from wtforms.widgets import PasswordInput

from eat.models.user import User

from . import EmailExists


class SignUp(Form):
    email = StringField('Email', [InputRequired(message=u'Email is required'),
                                  Email(message=u'Invalid email address.'),
                                  EmailExists(should_exist=False)])
    password = PasswordField('Password',
                             [InputRequired(message=u'Password is required')],
                             widget=PasswordInput(hide_value=False))
    redir_url = HiddenField(default=lambda: request.full_path)


class SignIn(SignUp):
    email = StringField('Email', [InputRequired(message=u'Email is required'),
                                  Email(message=u'Invalid email address.'),
                                  EmailExists()])

    def validate_password(self, field):
        """
        TODO: Prevent login bomb
        """
        user = self.get_user()
        if not user.verify_password(self.password.data):
            raise ValidationError('Incorrect Password')

    def get_user(self):
        return User.objects(email=self.email.data).first()
