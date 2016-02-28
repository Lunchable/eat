from flask_wtf import Form
from wtforms import StringField, BooleanField
from wtforms.validators import InputRequired, Length


class PersonForm(Form):
    first_name = StringField('First Name', [InputRequired()])
    middle_initial = StringField('Middle Initial')
    last_name = StringField('Last Name', [InputRequired()])


class ChildForm(PersonForm):
    school_postal = StringField('School Zip Code',
                                [InputRequired(), Length(min=5, max=15, message="Zip code must be 5-10 digits long")])
    school_city = StringField('School City', [InputRequired()])
    school_state = StringField('School State', [InputRequired()])
    school_name = StringField('School Name', [InputRequired()])


class ChildStatusForm(Form):
    foster = BooleanField(label='Foster Child')
    migrant = BooleanField(label='Migrant')
    homeless = BooleanField(label='Homeless')
    runaway = BooleanField(label='Runaway')
    headstart = BooleanField(label='Headstart')
