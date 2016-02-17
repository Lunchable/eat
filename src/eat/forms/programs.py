from flask_wtf import Form
from wtforms import SelectMultipleField, BooleanField
from wtforms.widgets import ListWidget, CheckboxInput

program_names = ['SNAP', 'TANF', 'FDPIR', 'FOSTER', 'MIGRANT', 'HOMELESS', 'RUNAWAY', 'HEADSTART']


class MultiCheckboxField(SelectMultipleField):
    widget = ListWidget(prefix_label=False)
    option_widget = CheckboxInput()


class ProgramsForm(Form):
    # programs = MultiCheckboxField('Program Participation', choices=program_names)
    SNAP = BooleanField()
    TANF = BooleanField()
    FDPIR = BooleanField()
    FOSTER = BooleanField()
    MIGRANT = BooleanField()
    HOMELESS = BooleanField()
    RUNAWAY = BooleanField()
    HEADSTART = BooleanField()
