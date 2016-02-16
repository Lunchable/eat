import bson.json_util as json
from bson import ObjectId
from flask import session, request, Response
from flask_login import current_user
from mongoengine.errors import DoesNotExist

from eat.models.application import Application, Applicant, Income, Child
from ..forms.applicant import ApplicantForm
from ..forms.income import IncomeForm
from ..forms.person import ChildForm


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
        for field in ['last_name', 'middle_initial', 'first_name', 'address_1',
                      'address_2', 'apt', 'city', 'state', 'postal', 'ssn']:
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

    @app.route('/svc/eat/v1/application/applicant/incomes', methods=['GET', 'POST'],
               endpoint='svc_eat_v1_application_applicant_incomes')
    @inject_application
    def svc_eat_v1_application_applicant_incomes(application):
        income_form = IncomeForm(csrf_enabled=False)
        if request.method == 'GET':
            if not application.applicant:
                return Response(
                    response=json.dumps({'errors': 'Applicant does not exist.'}),
                    status=404, headers=None,
                    content_type='application/json; charset=utf-8')

            if application.applicant and application.applicant.incomes:
                return json.dumps([i.dict for i in application.applicant.incomes])
            else:
                return Response(
                    response=json.dumps({'errors': 'Applicant income does not exist.', 'form': income_form.data}),
                    status=404, headers=None,
                    content_type='application/json; charset=utf-8')

        if not income_form.validate_on_submit():
            return Response(
                response=json.dumps({'errors': income_form.errors, 'form': income_form.data}),
                status=400, headers=None,
                content_type='application/json; charset=utf-8')

        income = Income()
        for field in ['source', 'amount', 'frequency']:
            if income_form.data[field]:
                income[field] = income_form.data[field]
        application.applicant.incomes.append(income)
        application.save()
        return Response(response=json.dumps(application.dict),
                        status=201, headers=None,
                        content_type='application/json; charset=utf-8')

    @app.route('/svc/eat/v1/application/applicant/incomes/<income_id>', methods=['GET', 'DELETE'],
               endpoint='svc_eat_v1_application_applicant_incomes_income_id')
    @inject_application
    def svc_eat_v1_application_applicant_incomes_income_id(application, income_id):
        application.applicant = application.applicant or Applicant()
        try:
            income = application.applicant.incomes.get(_id=ObjectId(income_id))

            if request.method == 'GET':
                return json.dumps(income.dict)
            else:
                application.applicant.incomes.remove(income)
                application.save()

            return Response(response=json.dumps(application.dict),
                            status=201, headers=None,
                            content_type='application/json; charset=utf-8')
        except DoesNotExist:
            return Response(
                response=json.dumps({'errors': 'Income does not exist.'}),
                status=404, headers=None,
                content_type='application/json; charset=utf-8')

        except Exception:
            return Response(
                response=json.dumps({'errors': 'The income could not be queried'}),
                status=404, headers=None,
                content_type='application/json; charset=utf-8')

    @app.route('/svc/eat/v1/application/children', methods=['GET', 'POST'],
               endpoint='svc_eat_v1_application_children')
    @inject_application
    def svc_eat_v1_application_children(application):
        child_form = ChildForm(csrf_enabled=False)
        if request.method == 'GET':
            if application.children:
                return json.dumps([c.dict for c in application.children])
            else:
                return Response(
                    response=json.dumps({'errors': 'Children do not exist.', 'form': child_form.data}),
                    status=404, headers=None,
                    content_type='application/json; charset=utf-8')

        if not child_form.validate_on_submit():
            return Response(
                response=json.dumps({'errors': child_form.errors, 'form': child_form.data}),
                status=400, headers=None,
                content_type='application/json; charset=utf-8')

        child = Child()
        for field in ['first_name', 'middle_initial', 'last_name', 'school_zip', 'school_city', 'school_state']:
            if child_form.data[field]:
                child[field] = child_form.data[field]
        application.children.append(child)
        application.save()
        return Response(response=json.dumps(application.dict),
                        status=201, headers=None,
                        content_type='application/json; charset=utf-8')

    @app.route('/svc/eat/v1/application/children/<child_id>', methods=['GET', 'DELETE'],
               endpoint='svc_eat_v1_application_children_child_id')
    @inject_application
    def svc_eat_v1_application_children_child_id(application, child_id):
        try:
            child = application.children.get(_id=ObjectId(child_id))

            if request.method == 'GET':
                return json.dumps(child.dict)
            else:
                application.children.remove(child)
                application.save()

            return Response(response=json.dumps(application.dict),
                            status=201, headers=None,
                            content_type='application/json; charset=utf-8')
        except DoesNotExist:
            return Response(
                response=json.dumps({'errors': 'Child does not exist.'}),
                status=404, headers=None,
                content_type='application/json; charset=utf-8')

        except Exception:
            return Response(
                response=json.dumps({'errors': 'The child could not be queried'}),
                status=404, headers=None,
                content_type='application/json; charset=utf-8')

    @app.route('/svc/eat/v1/application/children/<child_id>/incomes', methods=['GET', 'POST'],
               endpoint='svc_eat_v1_application_children_child_id_incomes')
    @inject_application
    def svc_eat_v1_application_children_child_id_incomes(application, child_id):
        income_form = IncomeForm(csrf_enabled=False)
        try:
            child = application.children.get(_id=ObjectId(child_id))

            if request.method == 'GET':
                return json.dumps([i.dict for i in child.incomes])
            else:
                if not income_form.validate_on_submit():
                    return Response(
                        response=json.dumps({'errors': income_form.errors, 'form': income_form.data}),
                        status=400, headers=None,
                        content_type='application/json; charset=utf-8')

                income = Income()
                for field in ['source', 'amount', 'frequency']:
                    if income_form.data[field]:
                        income[field] = income_form.data[field]
                child.incomes.append(income)
                application.save()

            return Response(response=json.dumps(application.dict),
                            status=201, headers=None,
                            content_type='application/json; charset=utf-8')
        except DoesNotExist:
            return Response(
                response=json.dumps({'errors': 'Child does not exist.'}),
                status=404, headers=None,
                content_type='application/json; charset=utf-8')

        except Exception:
            return Response(
                response=json.dumps({'errors': 'The child could not be queried'}),
                status=404, headers=None,
                content_type='application/json; charset=utf-8')

    @app.route('/svc/eat/v1/application/children/<child_id>/incomes/<income_id>', methods=['GET', 'DELETE'],
               endpoint='svc_eat_v1_application_children_child_id_incomes_income_id')
    @inject_application
    def svc_eat_v1_application_children_child_id_incomes_income_id(application, child_id, income_id):
        try:
            child = application.children.get(_id=ObjectId(child_id))
            income = child.incomes.get(_id=ObjectId(income_id))

            if request.method == 'GET':
                return json.dumps(income.dict)
            else:
                child.incomes.remove(income)
                application.save()

            return Response(response=json.dumps(application.dict),
                            status=201, headers=None,
                            content_type='application/json; charset=utf-8')
        except DoesNotExist:
            return Response(
                response=json.dumps({'errors': 'Income does not exist.'}),
                status=404, headers=None,
                content_type='application/json; charset=utf-8')

        except Exception:
            return Response(
                response=json.dumps({'errors': 'The income could not be queried'}),
                status=404, headers=None,
                content_type='application/json; charset=utf-8')
