import bson.json_util as json
from flask import session, request, Response
from flask_login import current_user

from eat.models.application import Application, Applicant
from ..forms.applicant import ApplicantForm


def register_routes(app):
    def inject_application(f):
        def decorator(**kwargs):
            application_id = session.get('application_id')
            if application_id:
                return f(Application.objects(id=application_id).first(), **kwargs)

            application = None

            if current_user.is_authenticated:
                # User may have applications they previously created
                # load the latest one into the session
                if current_user.applications:
                    for a in current_user.applications:
                        if not application:
                            application = a
                        else:
                            if a.created_at > application.created_at:
                                application = a
                    session['application_id'] = application.id
                else:
                    # Need to create a new application
                    application = Application()
                    application.save()
                    session['application_id'] = application.id
            else:
                # Need to create a new application
                application = Application()
                application.save()
                session['application_id'] = application.id

            return f(application, **kwargs)

        return decorator

    @app.route('/svc/eat/v1/application/applicant', methods=['GET', 'POST', 'PUT'],
               endpoint='svc_eat_v1_application_applicant')
    @inject_application
    def svc_eat_v1_application_applicant(application):
        applicant_form = ApplicantForm(csrf_enabled=False)
        if request.method == 'GET':
            if application.applicant:
                return json.dumps(application.applicant.dict)
            else:
                return Response(
                    response=json.dumps({'errors': 'Applicant does not exist.', 'form': applicant_form.data}),
                    status=404, headers=None,
                    content_type='application/json; charset=utf-8')
        elif request.method == 'POST' and application.applicant:
            return Response(response=json.dumps({'error': 'Applicant already exists.  Use PUT instead'}),
                            status=409, headers=None,
                            content_type='application/json; charset=utf-8')

        application.applicant = application.applicant or Applicant()
        if not applicant_form.validate_on_submit():
            return Response(
                response=json.dumps({'errors': applicant_form.errors, 'form': applicant_form.data}),
                status=400, headers=None,
                content_type='application/json; charset=utf-8')
        for field in ['middle_initial', 'city', 'last_name', 'first_name', 'apt', 'state', 'ssn', 'address_1',
                      'address_2', 'postal']:
            if applicant_form.data[field]:
                application.applicant[field] = applicant_form.data[field]
        application.save()
        return Response(response=json.dumps(application.dict),
                        status=201, headers=None,
                        content_type='application/json; charset=utf-8')

    @app.route('/svc/eat/v1/application', methods=['GET', 'POST'], endpoint='svc_eat_v1_application')
    @inject_application
    def svc_eat_v1_application(application):
        return json.dumps(application.dict)
