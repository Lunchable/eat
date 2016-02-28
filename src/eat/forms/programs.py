from flask_wtf import Form
from wtforms import BooleanField


class ChildStatusForm(Form):
    foster = BooleanField(label='Foster Child')
    migrant = BooleanField(label='Migrant')
    homeless = BooleanField(label='Homeless')
    runaway = BooleanField(label='Runaway')
    headstart = BooleanField(label='Headstart')
