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

# Define the blueprint: 'profile', set its url prefix: app.url/profile
mod_profile = Blueprint('profile', __name__, url_prefix='/profile')

@mod_profile.route('/', methods=['GET', 'POST'])
def profile():
    return render_template('profile/profile.html')
