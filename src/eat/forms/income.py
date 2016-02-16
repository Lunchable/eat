from flask_wtf import Form
from wtforms import StringField, DecimalField
from wtforms.validators import InputRequired, AnyOf


class IncomeForm(Form):
    # TODO: validate source against known values
    source = StringField('Source', [InputRequired()])
    amount = DecimalField('Amount', [InputRequired()])
    frequency = StringField('Frequency', [InputRequired(), AnyOf(values=['daily', 'weekly', 'biweekly', 'semimonthly', 'monthly'])])
