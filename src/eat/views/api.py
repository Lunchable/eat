import bson.json_util as json
from bson import ObjectId
from flask import session, request, Response
from flask_login import current_user
from mongoengine.errors import DoesNotExist
import pickle

from eat.models.application import Application, Applicant, Income, Child, Program, Ethnicity, Person
from ..forms.applicant import ApplicantForm
from ..forms.income import IncomeForm
from ..forms.person import ChildForm, PersonForm
from ..forms.programs import ProgramsForm
from ..forms.ethnicity import EthnicityForm


def inject_application(f):
    def decorator(**kwargs):
        application = None
        application_id = session.get('application_id')
        if application_id:
            application = Application.objects(id=application_id).first()
        if application:
            response = f(application, **kwargs)
            return response

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
            application.applicant = Applicant()
            application.save()
            session['application_id'] = application.id

        response = f(application, **kwargs)
        return response

    return decorator


def register_routes(app):
    @app.route('/svc/eat/v1/application/applicant', methods=['GET', 'POST'],
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

        application.applicant = application.applicant or Applicant()
        if not applicant_form.validate_on_submit():
            return Response(
                response=json.dumps({'errors': applicant_form.errors, 'form': applicant_form.data}),
                status=400, headers=None,
                content_type='application/json; charset=utf-8')
        for field in ['last_name', 'middle_initial', 'first_name', 'address_1',
                      'address_2', 'apt', 'city', 'state', 'postal', 'ssn']:
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
        return Response(response=json.dumps(income.dict),
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

            return Response(response=None,
                            status=204, headers=None)
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
        for field in ['first_name', 'middle_initial', 'last_name', 'school_postal', 'school_city', 'school_state',
                      'school_name']:
            if child_form.data[field]:
                child[field] = child_form.data[field]
        application.children.append(child)
        application.save()
        return Response(response=json.dumps(child.dict),
                        status=201, headers=None,
                        content_type='application/json; charset=utf-8')

    @app.route('/svc/eat/v1/application/children/<child_id>', methods=['GET', 'POST', 'DELETE'],
               endpoint='svc_eat_v1_application_children_child_id')
    @inject_application
    def svc_eat_v1_application_children_child_id(application, child_id):
        child_form = ChildForm(csrf_enabled=False)
        try:
            child = application.children.get(_id=ObjectId(child_id))

            if request.method == 'GET':
                return json.dumps(child.dict)
            elif request.method == 'POST':
                if not child_form.validate_on_submit():
                    return Response(
                        response=json.dumps({'errors': child_form.errors, 'form': child_form.data}),
                        status=400, headers=None,
                        content_type='application/json; charset=utf-8')
                for field in ['first_name', 'middle_initial', 'last_name', 'school_postal', 'school_city',
                              'school_state', 'school_name']:
                    child[field] = child_form.data[field]
                application.save()

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

            return Response(response=json.dumps(income.dict),
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

    @app.route('/svc/eat/v1/application/children/<child_id>/programs', methods=['GET', 'POST'],
               endpoint='svc_eat_v1_application_children_child_id_programs')
    @inject_application
    def svc_eat_v1_application_children_child_id_programs(application, child_id):
        programs_form = ProgramsForm(csrf_enabled=False)
        try:
            child = application.children.get(_id=ObjectId(child_id))

            if request.method == 'GET':
                return json.dumps([p.dict for p in child.programs])
            else:
                if not programs_form.validate_on_submit():
                    return Response(
                        response=json.dumps({'errors': programs_form.errors, 'form': programs_form.programs.data}),
                        status=400, headers=None,
                        content_type='application/json; charset=utf-8')

                programs = [Program(program_name=p) for (p, k) in programs_form.data.items() if k]
                child.programs = programs
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

    @app.route('/svc/eat/v1/application/children/<child_id>/ethnicities', methods=['GET', 'POST'],
               endpoint='svc_eat_v1_application_children_child_id_ethnicities')
    @inject_application
    def svc_eat_v1_application_children_child_id_ethnicities(application, child_id):
        ethnicities_form = EthnicityForm(csrf_enabled=False)
        try:
            child = application.children.get(_id=ObjectId(child_id))

            if request.method == 'GET':
                return json.dumps([p.dict for p in child.ethnicities])
            else:
                if not ethnicities_form.validate_on_submit():
                    return Response(
                        response=json.dumps(
                            {'errors': ethnicities_form.errors, 'form': ethnicities_form.ethnicities.data}),
                        status=400, headers=None,
                        content_type='application/json; charset=utf-8')

                ethnicities = [Ethnicity(ethnicity_name=p) for (p, k) in ethnicities_form.data.items() if k]
                child.ethnicities = ethnicities
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

    @app.route('/svc/eat/v1/application/persons', methods=['GET', 'POST'],
               endpoint='svc_eat_v1_application_persons')
    @inject_application
    def svc_eat_v1_application_persons(application):
        person_form = PersonForm(csrf_enabled=False)
        if request.method == 'GET':
            if application.persons:
                return json.dumps([c.dict for c in application.persons])
            else:
                return Response(
                    response=json.dumps({'errors': 'Persons do not exist.', 'form': person_form.data}),
                    status=404, headers=None,
                    content_type='application/json; charset=utf-8')

        if not person_form.validate_on_submit():
            return Response(
                response=json.dumps({'errors': person_form.errors, 'form': person_form.data}),
                status=400, headers=None,
                content_type='application/json; charset=utf-8')

        person = Person()
        for field in ['first_name', 'middle_initial', 'last_name']:
            if person_form.data[field]:
                person[field] = person_form.data[field]
        application.persons.append(person)
        application.save()
        return Response(response=json.dumps(application.dict),
                        status=201, headers=None,
                        content_type='application/json; charset=utf-8')

    @app.route('/svc/eat/v1/application/persons/<person_id>', methods=['GET', 'DELETE'],
               endpoint='svc_eat_v1_application_persons_person_id')
    @inject_application
    def svc_eat_v1_application_persons_person_id(application, person_id):
        try:
            person = application.persons.get(_id=ObjectId(person_id))

            if request.method == 'GET':
                return json.dumps(person.dict)
            else:
                application.persons.remove(person)
                application.save()

            return Response(response=json.dumps(application.dict),
                            status=201, headers=None,
                            content_type='application/json; charset=utf-8')
        except DoesNotExist:
            return Response(
                response=json.dumps({'errors': 'Person does not exist.'}),
                status=404, headers=None,
                content_type='application/json; charset=utf-8')

        except Exception:
            return Response(
                response=json.dumps({'errors': 'The person could not be queried'}),
                status=404, headers=None,
                content_type='application/json; charset=utf-8')

    @app.route('/svc/eat/v1/application/persons/<person_id>/incomes', methods=['GET', 'POST'],
               endpoint='svc_eat_v1_application_persons_person_id_incomes')
    @inject_application
    def svc_eat_v1_application_persons_person_id_incomes(application, person_id):
        income_form = IncomeForm(csrf_enabled=False)
        try:
            person = application.persons.get(_id=ObjectId(person_id))

            if request.method == 'GET':
                return json.dumps([i.dict for i in person.incomes])
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
                person.incomes.append(income)
                application.save()

            return Response(response=json.dumps(application.dict),
                            status=201, headers=None,
                            content_type='application/json; charset=utf-8')
        except DoesNotExist:
            return Response(
                response=json.dumps({'errors': 'Person does not exist.'}),
                status=404, headers=None,
                content_type='application/json; charset=utf-8')

        except Exception:
            return Response(
                response=json.dumps({'errors': 'The person could not be queried'}),
                status=404, headers=None,
                content_type='application/json; charset=utf-8')

    @app.route('/svc/eat/v1/application/persons/<person_id>/incomes/<income_id>', methods=['GET', 'DELETE'],
               endpoint='svc_eat_v1_application_persons_person_id_incomes_income_id')
    @inject_application
    def svc_eat_v1_application_persons_person_id_incomes_income_id(application, person_id, income_id):
        try:
            person = application.persons.get(_id=ObjectId(person_id))
            income = person.incomes.get(_id=ObjectId(income_id))

            if request.method == 'GET':
                return json.dumps(income.dict)
            else:
                person.incomes.remove(income)
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

    @app.route('/svc/eat/v1/application/persons/<person_id>/programs', methods=['GET', 'POST'],
               endpoint='svc_eat_v1_application_persons_person_id_programs')
    @inject_application
    def svc_eat_v1_application_persons_person_id_programs(application, person_id):
        programs_form = ProgramsForm(csrf_enabled=False)
        try:
            person = application.persons.get(_id=ObjectId(person_id))

            if request.method == 'GET':
                return json.dumps([p.dict for p in person.programs])
            else:
                if not programs_form.validate_on_submit():
                    return Response(
                        response=json.dumps({'errors': programs_form.errors, 'form': programs_form.programs.data}),
                        status=400, headers=None,
                        content_type='application/json; charset=utf-8')

                programs = [Program(program_name=p) for (p, k) in programs_form.data.items() if k]
                person.programs = programs
                application.save()

            return Response(response=json.dumps(application.dict),
                            status=201, headers=None,
                            content_type='application/json; charset=utf-8')
        except DoesNotExist:
            return Response(
                response=json.dumps({'errors': 'Person does not exist.'}),
                status=404, headers=None,
                content_type='application/json; charset=utf-8')

        except Exception:
            return Response(
                response=json.dumps({'errors': 'The person could not be queried'}),
                status=404, headers=None,
                content_type='application/json; charset=utf-8')

    @app.route('/svc/eat/v1/application/persons/<person_id>/ethnicities', methods=['GET', 'POST'],
               endpoint='svc_eat_v1_application_persons_person_id_ethnicities')
    @inject_application
    def svc_eat_v1_application_persons_person_id_ethnicities(application, person_id):
        ethnicities_form = EthnicityForm(csrf_enabled=False)
        try:
            person = application.persons.get(_id=ObjectId(person_id))

            if request.method == 'GET':
                return json.dumps([p.dict for p in person.ethnicities])
            else:
                if not ethnicities_form.validate_on_submit():
                    return Response(
                        response=json.dumps(
                            {'errors': ethnicities_form.errors, 'form': ethnicities_form.ethnicities.data}),
                        status=400, headers=None,
                        content_type='application/json; charset=utf-8')

                ethnicities = [Ethnicity(ethnicity_name=p) for (p, k) in ethnicities_form.data.items() if k]
                person.ethnicities = ethnicities
                application.save()

            return Response(response=json.dumps(application.dict),
                            status=201, headers=None,
                            content_type='application/json; charset=utf-8')
        except DoesNotExist:
            return Response(
                response=json.dumps({'errors': 'Person does not exist.'}),
                status=404, headers=None,
                content_type='application/json; charset=utf-8')

        except Exception:
            return Response(
                response=json.dumps({'errors': 'The person could not be queried'}),
                status=404, headers=None,
                content_type='application/json; charset=utf-8')
