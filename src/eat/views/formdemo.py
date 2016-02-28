from flask import redirect
from flask import render_template
from flask_login import current_user, login_user, logout_user

from eat.forms.auth import SignIn, SignUp
from eat.forms.income import IncomeForm
from eat.forms.applicant import ApplicantForm
from eat.forms.person import PersonForm, ChildForm, ChildStatusForm
from eat.forms.ethnicity import EthnicityForm
from eat.models.user import User
from .api import inject_application


def register_routes(app):
    @app.route('/application', methods=['GET'], endpoint='_application')
    @inject_application
    def _application(application):
        return render_template('application.html', application=application, ApplicantForm=ApplicantForm,
                               IncomeForm=IncomeForm, PersonForm=PersonForm, EthnicityForm=EthnicityForm,
                               ChildStatusForm=ChildStatusForm,
                               ChildForm=ChildForm)
