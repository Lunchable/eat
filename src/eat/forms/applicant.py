from flask_wtf import Form
from wtforms import StringField, SelectField
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
    state = frequency = SelectField('State',
                                    choices=[('AK', 'AK'), ('AL', 'AL'), ('AR', 'AR'), ('AZ', 'AZ'), ('CA', 'CA'),
                                             ('CO', 'CO'), ('CT', 'CT'), ('DC', 'DC'), ('DE', 'DE'), ('FL', 'FL'),
                                             ('GA', 'GA'), ('HI', 'HI'),
                                             ('IA', 'IA'), ('ID', 'ID'), ('IL', 'IL'), ('IN', 'IN'), ('KS', 'KS'),
                                             ('KY', 'KY'), ('LA', 'LA'), ('MA', 'MA'), ('MD', 'MD'), ('ME', 'ME'),
                                             ('MI', 'MI'), ('MN', 'MN'),
                                             ('MO', 'MO'), ('MS', 'MS'), ('MT', 'MT'), ('NC', 'NC'), ('ND', 'ND'),
                                             ('NE', 'NE'), ('NH', 'NH'), ('NJ', 'NJ'), ('NM', 'NM'), ('NV', 'NV'),
                                             ('NY', 'NY'), ('OH', 'OH'),
                                             ('OK', 'OK'), ('OR', 'OR'), ('PA', 'PA'), ('PR', 'PR'), ('RI', 'RI'),
                                             ('SC', 'SC'), ('SD', 'SD'), ('TN', 'TN'), ('TX', 'TX'), ('UT', 'UT'),
                                             ('VA', 'VA'), ('VT', 'VT'),
                                             ('WA', 'WA'), ('WI', 'WI'), ('WV', 'WV'), ('WY', 'WY')])

    snap_case = StringField('SNAP Case #')
    tanf_case = StringField('TANF Case #')
    fdipr_case = StringField('FDIPR Case #')
