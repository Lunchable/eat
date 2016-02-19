from flask_wtf import Form
from wtforms import DecimalField, SelectField
from wtforms.validators import InputRequired


class IncomeForm(Form):
    source = SelectField('Source', choices=[('wages', 'Wages'), ('tips', 'Tips')])
    amount = DecimalField('Amount', [InputRequired()])
    frequency = SelectField('Frequency',
                            choices=[('daily', 'Daily'), ('weekly', 'Weekly'), ('biweekly', 'Every Two Weeks'),
                                     ('semimonthly', 'Twice a Month'), ('monthly', 'Monthly'), ('annual', 'Annually')])
