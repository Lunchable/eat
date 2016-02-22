from flask_wtf import Form
from wtforms import BooleanField

program_names = ['SNAP', 'TANF', 'FDPIR', 'FOSTER', 'MIGRANT', 'HOMELESS', 'RUNAWAY', 'HEADSTART']


class ProgramsForm(Form):
    SNAP = BooleanField(label='SNAP')
    TANF = BooleanField(label='TANF')
    FDPIR = BooleanField(label='FDPIR')
    FOSTER = BooleanField(label='Foster Child')
    MIGRANT = BooleanField(label='Migrant')
    HOMELESS = BooleanField(label='Homeless')
    RUNAWAY = BooleanField(label='Runaway')
    HEADSTART = BooleanField(label='Headstart')
