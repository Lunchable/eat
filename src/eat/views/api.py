import bson.json_util as json
from flask import redirect
from flask import session
from flask_login import current_user

from eat.models.application import Application


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

    @app.route('/svc/eat/v1/name', methods=['GET', 'POST'])
    def api_name():
        return redirect('/')

    @app.route('/svc/eat/v1/application/applicant', methods=['GET', 'POST'],
               endpoint='svc_eat_v1_application_applicant')
    @inject_application
    def svc_eat_v1_application_applicant(application):
        if application.applicant:
            return json.dumps(application.applicant.dict)
        else:
            return json.dumps({})

    @app.route('/svc/eat/v1/application', methods=['GET', 'POST'], endpoint='svc_eat_v1_application')
    @inject_application
    def svc_eat_v1_application(application):
        return json.dumps(application.dict)
