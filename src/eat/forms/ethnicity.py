from flask_wtf import Form
from wtforms import BooleanField


class EthnicityForm(Form):
    hispanic_or_latino = BooleanField(label='Hispanic or Latino')
    native_american = BooleanField(label='American Indian or Alaska Native')
    asian = BooleanField(label='Asian')
    black_or_african_american = BooleanField(label='Black or African American')
    pacific_islander = BooleanField(label='Native Hawaiian or Other Pacific Islander')
    white = BooleanField(label='White')
    decline = BooleanField(label='Decline to Answer')
