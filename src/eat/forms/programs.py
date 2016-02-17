from flask_wtf import Form
from wtforms import BooleanField

program_names = ['SNAP', 'TANF', 'FDPIR', 'FOSTER', 'MIGRANT', 'HOMELESS', 'RUNAWAY', 'HEADSTART']


class ProgramsForm(Form):
    SNAP = BooleanField()
    TANF = BooleanField()
    FDPIR = BooleanField()
    FOSTER = BooleanField()
    MIGRANT = BooleanField()
    HOMELESS = BooleanField()
    RUNAWAY = BooleanField()
    HEADSTART = BooleanField()
