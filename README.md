# eat
Electronic Application Transformation - a model electronic application for the National School Lunch Program.  http://lunchux.devpost.com

# Code of Conduct
This project adheres to the [Open Code of Conduct][code-of-conduct]. By participating, you are expected to honor this code.
[code-of-conduct]: code-of-conduct.md

# Prerequisites
1. Python 2.7
2. Mongodb

# Running the app locally
1. create and activate your virtualenv
2. pip install -r requirements
3. cd src && python manage.py runserver

# API interface

All operations load the user's latest application into the session, or create a new application for the user.  Since we expect new users to be anonymous at first, the application will exist in the database and in the session, but will not be tied to a user.  If the anonymous user leaves for 24 hours, the session is gone, and the application is permanently orphaned.

If the user signs up or logs in at any time during or after the process, the new application will be associated with that user.  If the user already had an existing application, the latest one to be created will take precedence, since we don't have a method for letting a user manage multiple applications yet.

All forms are validated server-side, and return 400 status with error descriptions if validation fails.

```
pGET /svc/eat/v1/application
```
Returns the application object stored in the session.

---
```
GET /svc/eat/v1/application/applicant
```
Returns the application's applicant info if it exists, or a 404 if it doesn't exist yet

---
```
POST /svc/eat/v1/application/applicant
```
(form eat.forms.applicant.Applicant)
If the application's applicant info doesn't exist, it will create and return the entire application.
If it does exist, it will return a 409 conflict.

---
```
PUT /svc/eat/v1/application/applicant
```
(form eat.forms.applicant.Applicant)
Overwrites all top-level fields on an existing applicant object

---
```
GET /svc/eat/v1/application/applicant/incomes
```
Returns a 404 if the applicant's info doesn't exist yet.
Returns a list of all the applicant's incomes

---
```
POST /svc/eat/v1/application/applicant/incomes
```
(form eat.forms.applicant.Income)
Returns a 404 if the applicant's info doesn't exist yet.
Creates a new income object, and returns the entire application object

---
```
GET /svc/eat/v1/application/applicant/incomes/<income_id>
```
Returns a 404 if the applicant's info doesn't exist yet, or if an income object with that income_id doesn't exist on the application.
Returns the income object with that income_id

---
```
DELETE /svc/eat/v1/application/applicant/incomes/<income_id>
```
Returns a 404 if the applicant's info doesn't exist yet, or if an income object with that income_id doesn't exist on the application.
Deletes the income object and returns the entire application object.

---
```
GET /svc/eat/v1/application/children
```
Returns a 404 if there are no children on the application
Returns a list of child objects


---
```
POST /svc/eat/v1/application/children
```
(form eat.forms.person.ChildForm)
Creates a new child object and attaches it to the application

---
```
GET /svc/eat/v1/application/children/<child_id>
```
Returns a 404 if a child does not exist whose id is child_id
Returns the child object

---
```
DELETE /svc/eat/v1/application/children/<child_id>
```
Returns a 404 if a child does not exist whose id is child_id
Deletes the child object and returns the application.

---
```
GET /svc/eat/v1/application/children/<child_id>/incomes
```
Returns a 404 if a child does not exist whose id is child_id
Returns a list of the child's incomes

---
```
POST /svc/eat/v1/application/children/<child_id>/incomes
```
(form eat.forms.applicant.Income)
Returns a 404 if a child does not exist whose id is child_id
Creates a new income object attached to the child, and returns the entire application object

---
```
GET /svc/eat/v1/application/children/<child_id>/incomes/<income_id>
```
Returns a 404 if a child does not exist whose id is child_id, or if the child's income whose id is income_id does not exist
Returns the child's income object

---
```
DELETE /svc/eat/v1/application/children/<child_id>/incomes/<income_id>
```
Returns a 404 if a child does not exist whose id is child_id, or if the child's income whose id is income_id does not exist
Deletes the child's income object and returns the application.


