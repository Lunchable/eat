from flask_wtf import Form
from wtforms import StringField
from wtforms.validators import InputRequired


class ApplicantForm(Form):
    first_name = StringField('First Name', [InputRequired()])
    middle_initial = StringField('Middle Initial')
    last_name = StringField('Last Name', [InputRequired()])
    ssn = StringField('SSN', [InputRequired()])
    address_1 = StringField('Address 1', [InputRequired()])
    address_2 = StringField('Address 2')
    apt = StringField('Apt #')
    postal = StringField('Zip Code', [InputRequired()])
    city = StringField('City', [InputRequired()])
    state = StringField('State', [InputRequired()])
