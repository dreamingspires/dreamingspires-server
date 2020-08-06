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

import app.extensions.sidebar as sb

# Import module forms
from app.mod_profile.forms import generate_developer_profile_form

# Define the blueprint: 'profile', set its url prefix: app.url/profile
mod_profile = Blueprint('profile', __name__, url_prefix='/profile')

@mod_profile.route('/', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = generate_developer_profile_form(current_user)
    if form.validate_on_submit:
        pass

    # Generate sidebar
    organisations = {}
    if current_user.departments:
        for department in current_user.departments:
            try:
                organisations[department.organisation.display_name]
            except KeyError:
                organisations[department.organisation.display_name] = {
                    'link': url_for('profile.edit_organisation', 
                        id=department.organisation.id),
                    'departments': {}
                }
            organisations[department.organisation.display_name]['departments']\
                [department.display_name] = {
                    'link': url_for('profile.edit_department',
                        id=department.id)
                }
    return render_template('profile/profile.html', user=current_user, \
            organisations=organisations, form=form)

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
    form = generate_developer_profile_form(current_user)
    return render_template('profile/developer_profile.html', form=form)

@mod_profile.route('/join_organisation/', methods=['GET', 'POST'])
@login_required
def join_organisation():
    form = generate_developer_profile_form(current_user)
    return render_template('profile/developer_profile.html', form=form)
