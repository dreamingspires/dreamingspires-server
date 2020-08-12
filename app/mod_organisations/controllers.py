# Import flask dependencies
from flask import Blueprint, request, render_template, render_template_string, \
                  flash, g, session, redirect, url_for
from flask_login import login_user, logout_user, login_required, current_user
from flask_navigation import Navigation

# Import the database object from the main app module
from app import db

from app.mod_organisations.forms import CreateProjectForm

# Import module models (i.e. Projects)
from app.models import Project, Organisation, Department, DepartmentFile
from app.mod_organisations.forms import generate_edit_organisation_form

# Define the blueprint: 'auth', set its url prefix: app.url/auth
mod_organisations = Blueprint('organisations', __name__, url_prefix='/org')

@mod_organisations.route('/<organisation_id>')
def organisation(organisation_id):
    return(f'Organisation: {organisation_id}')

@mod_organisations.route('/organisation/<organisation_id>/create')
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

@mod_organisations.route('/department/<department_id>')
def department(department_id):
    return(f'Department: {department_id}')

# TODO: move actual department creation here
#@mod_organisations.route('/<organisation_id>/<department_id>/create')
#def create_department(organisation_id, department_id):
#    org = Organisation.query.filter_by(id=organisation_id).first()
#    if not org:
#        return(f'Organisation {organisation_id} does not exist')
#
#    dep = Department.query.filter_by(id=department_id).first()
#    if dep:
#        return(f'Department exists: {organisation_id}/{department_id}')
#    else:
#        # Create the department
#        department = Department(id=department_id, \
#            display_name=department_id, description="", \
#            organisation=org)
#        db.session.add(department)
#        db.session.commit()
#        return(f'Organisation created: {department_id}')

@mod_organisations.route('/edit_department/<department_id>', \
    methods=['GET', 'POST'])
@login_required
def edit_department(department_id):
    dep = Department.query.filter_by(id=department_id).first()
    # Test to make sure person is owner of department
    if current_user not in dep.users:
        # Forbidden
        return 'Forbidden'
    
    form = generate_edit_organisation_form(dep)
    if not dep:
        return(f'Department {department_id} does not exist')

    if form.validate_on_submit():
        dep.description = form.description.data
        if form.display_image.data:
            try:
                dep.display_image = form.display_image.data
            except PIL.UnidentifiedImageError:
                # TODO: pretty up error page
                return "Error: Uploaded file is not an image"

        # Ugly hack because checking if data==None for MultipleFileField
        # doesn't work - it always returns an empty, garbage file
        if form.supporting_evidence.data[0].filename:
            files = [DepartmentFile(document=f) for f in \
                form.supporting_evidence.data]
            for f in files:
                dep.supporting_evidence.append(f)

        db.session.add(dep)
        db.session.commit()

        print('redirecting to: {}'.format(url_for('organisations.edit_department', \
            department_id=department_id)))
        return redirect(url_for('organisations.edit_department', \
            department_id=department_id))

    return render_template('organisations/department.html', \
        dep=dep, form=form)
    

@mod_organisations.route('/<department_id>/create_project/', \
        methods=['GET', 'POST'])
@login_required
def create_project(department_id):
    # Ensure the current user is a member of the department
    dep = Department.query.filter_by(id=department_id).first()
    if not dep:
        return(f'Department {department_id} does not exist')
    if current_user not in dep.users:
        return('Forbidden')

    form = CreateProjectForm()
    if form.validate_on_submit():
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
