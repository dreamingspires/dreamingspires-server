# Import flask dependencies
from flask import Blueprint, request, render_template, \
                  flash, g, session, redirect, url_for, current_app, abort
from flask_login import login_user, logout_user, login_required, current_user
from flask_principal import Principal, Identity, AnonymousIdentity, \
     identity_changed
from is_safe_url import is_safe_url

# Import password / encryption helper tools
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug import secure_filename

# Import the database object from the main app module
from app import db
from depot.manager import DepotManager

import app.extensions.sidebar as sb
from app.models import Department, Organisation, User
import app.types as t

# Import module forms
from app.mod_profile.forms import generate_edit_user_public_profile_form, \
    CreateDepartmentForm

# Define the blueprint: 'profile', set its url prefix: app.url/profile
mod_profile = Blueprint('profile', __name__, url_prefix='/profile')

import PIL

@mod_profile.route('/', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = generate_edit_user_public_profile_form(current_user)
    if form.validate_on_submit():
        display_name = form.display_name.data if form.display_name.data != '' \
            else current_user.display_name
        current_user.display_name = display_name
        current_user.description = form.description.data

        if form.university_check.data:
            current_user.educational_institution = None \
                if form.university.data == '' else form.university.data
        else:
            current_user.educational_institution = None

        # TODO: update profile picture
        if form.display_image:
            try:
                current_user.display_image = form.display_image.data
            except PIL.UnidentifiedImageError:
                # TODO: pretty up error page
                return "Error: Uploaded file is not an image"

        db.session.add(current_user)
        db.session.commit()
        return redirect(url_for('profile.edit_profile'))

    # Generate sidebar
    organisations = {}
    if current_user.departments:
        for department in current_user.departments:
            try:
                display_name = department.organisation.display_name
                organisations[display_name]
            except AttributeError:
                if department.temp_organisation is None:
                    # We have a consistency error!
                    continue
                display_name = department.temp_organisation
                organisations[display_name] = {
                    # TODO: make this the pending organisation page
                    'link': None,
                    'departments': {}
                }
            except KeyError:
                organisations[display_name] = {
                    'link': url_for('profile.edit_organisation', 
                        id=department.organisation.id),
                    'departments': {}
                }
            organisations[display_name]['departments']\
                [department.display_name] = {
                    'link': url_for('profile.edit_department',
                        id=department.id)
                }
    return render_template('profile/profile.html', user=current_user, \
            organisations=organisations, form=form)

@mod_profile.route('/create_department/', methods=['GET', 'POST'])
@login_required
def create_department():
    form = CreateDepartmentForm()
    if not current_user.can_create_departments:
        return 'TODO: Error page'

    # Ensure the user has no other pending organisation applications
    for dep in current_user.departments:
        if dep.verification_status == t.VerificationStatus.pending:
            return "You cannot register more than one organisation at once"

    if form.validate_on_submit():

        # Find the corresponding organisation
        org = Organisation.query.filter_by(
            display_name=form.organisation_name.data).first()

        # Create a pending department
        dep = Department(
            display_name=form.department_name.data,
            description='',
            users=[current_user],
            organisation=org,
            verification_status=t.VerificationStatus.pending,
            temp_organisation=form.organisation_name.data if org is None \
                else None)

        db.session.add(dep)
        db.session.commit()

        return redirect(url_for('profile.edit_profile'))
    return render_template('profile/create_department.html', form=form)

@mod_profile.route('/edit_organisation/<id>', methods=['GET', 'POST'])
@login_required
def edit_organisation(id):
    return f'Edit organisation: {id}'

@mod_profile.route('/edit_department/<id>', methods=['GET', 'POST'])
@login_required
def edit_department(id):
    return f'Edit department: {id}'

@mod_profile.route('/developer/', methods=['GET', 'POST'])
@login_required
def developer():
    form = generate_edit_user_public_profile_form(current_user)
    return render_template('profile/developer_profile.html', form=form)

@mod_profile.route('/join_organisation/', methods=['GET', 'POST'])
@login_required
def join_organisation():
    form = generate_edit_user_public_profile_form(current_user)
    return render_template('profile/developer_profile.html', form=form)
