# Import flask dependencies
from flask import Blueprint, request, render_template, render_template_string, \
                  flash, g, session, redirect, url_for
from flask_navigation import Navigation

# Import the database object from the main app module
from app import db

from app.mod_organisations.forms import CreateProjectForm

# Import module models (i.e. Projects)
from app.models import Project, Organisation, Department

# Define the blueprint: 'auth', set its url prefix: app.url/auth
mod_organisations = Blueprint('organisations', __name__, url_prefix='/org')

@mod_organisations.route('/<organisation_id>')
def organisation(organisation_id):
    return(f'Organisation: {organisation_id}')

@mod_organisations.route('/<organisation_id>/create')
def create_organisation(organisation_id):
    org = Organisation.query.filter_by(id=organisation_id).first()
    if org:
        return(f'Organisation exists: {organisation_id}')
    else:
        # Create the organisation
        organisation = Organisation(id=organisation_id, \
            display_name=organisation_id, description="")
        db.session.add(organisation)
        db.session.commit()
        return(f'Organisation created: {organisation_id}')

@mod_organisations.route('/<organisation_id>/<department_id>')
def department(organisation_id, department_id):
    return(f'Department: {organisation_id}/{department_id}')

@mod_organisations.route('/<organisation_id>/<department_id>/create')
def create_department(organisation_id, department_id):
    org = Organisation.query.filter_by(id=organisation_id).first()
    if not org:
        return(f'Organisation {organisation_id} does not exist')

    dep = Department.query.filter_by(id=department_id).first()
    if dep:
        return(f'Department exists: {organisation_id}/{department_id}')
    else:
        # Create the department
        department = Department(id=department_id, \
            display_name=department_id, description="", \
            organisation=org)
        db.session.add(department)
        db.session.commit()
        return(f'Organisation created: {department_id}')

@mod_organisations.route('/<organisation_id>/<department_id>/create_project/', \
        methods=['GET', 'POST'])
def create_project(organisation_id, department_id):
    form = CreateProjectForm()
    if form.validate_on_submit():
        org = Organisation.query.filter_by(id=organisation_id).first()
        if not org:
            return(f'Organisation {organisation_id} does not exist')

        dep = Department.query.filter_by(id=department_id).first()
        if not dep:
            return(f'Department {organisation_id}/{department_id} does not exist')

        # Create the project
        project = Project(display_name=form.display_name.data,
            description=form.description.data,
            price=form.price.data,
            department=dep)
        db.session.add(project)
        db.session.commit()
        print('created project')
        return(f'Project created')

    return render_template('organisations/create_project.html', form=form)
