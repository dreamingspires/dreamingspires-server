# Import flask dependencies
from flask import Blueprint, request, render_template, \
                  flash, g, session, redirect, url_for, current_app, abort
from flask_login import login_user, logout_user, login_required, current_user
from flask_principal import Principal, Identity, AnonymousIdentity, \
     identity_changed
from is_safe_url import is_safe_url
from flask_socketio import send, emit
from datetime import datetime

# Import password / encryption helper tools
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.exceptions import Unauthorized
from werkzeug import secure_filename

# Import the database object from the main app module
from app import app, db, socketio

# Import module forms
from app.mod_auth.forms import LoginForm, RegisterDeveloperForm, \
    RegisterClientForm

# Import module models (i.e. User)
#from app.mod_auth.models import User, Email, Matrix, CV, Developer, \
#    Organisation, Project
from app.models import User, Email, Matrix, CV, Developer, \
    Organisation, Project

# Import extensions
from app.extensions.socketio_helpers import authenticated_only
from app.extensions.token import generate_confirmation_token, confirm_token
from app.extensions.email import send_email

# Define the blueprint: 'auth', set its url prefix: app.url/auth
mod_auth = Blueprint('auth', __name__, url_prefix='/auth')

# Set the route and accepted methods
@mod_auth.route('/login/', methods=['GET', 'POST'])
def login():
    # If sign in form is submitted
    form = LoginForm(request.form)

    # Verify the sign in form
    if form.validate_on_submit():
        print('form validated')
        user = User.query.filter_by(primary_email=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            if not user.email_verified:
                return render_template('auth/not_yet_activated.html')

            # Keep the user info in the session using Flask-Login
            login_user(user, remember=form.remember_me.data)

            next = request.args.get('next')
            #if not is_safe_url(next):
            #    return abort(400)
            return redirect(next or url_for('profile.landing_page'))

        flash('Wrong email or password', 'danger')

    return render_template('auth/login.html', form=form)

# Allow socket connections once logged in
@socketio.on('connect')
def connect_handler():
    if current_user.is_authenticated:
        # Store the session id in the cookie
        session['socketio_sid'] = request.sid
        #emit('my response',
        #     {'message': '{0} has joined'.format(current_user.display_name)})
    else:
        print('not authenticated yet')
        return False  # not allowed here

@socketio.on('my event')
@authenticated_only
def my_event(arg1):
    print('"my event" occurred')

@mod_auth.route('/logout/', methods=['GET', 'POST'])
@login_required
def logout():
    # Remove the user information from the session
    logout_user()

    # Remove session keys set by Flask-Principal
    #for key in ('identity.name', 'identity.auth_type'):
    #    session.pop(key, None)

    # Tell Flask-Principal the user is anonymous
    #identity_changed.send(current_app._get_current_object(),
    #                      identity=AnonymousIdentity())
    return redirect(request.args.get('next') or url_for('index'))

@mod_auth.route('/register_developer/', methods=['GET', 'POST'])
def register_developer():
    form = RegisterDeveloperForm()
    if form.validate_on_submit():
        # Check username is not already taken
        if User.query.filter_by(primary_email=form.email.data).first():
            flash('An account has already been registered with this email address.')
        elif User.query.filter_by(id=form.user_name.data).first():
            flash('Username already taken.')
        else:
            cv = CV(document=form.upload_cv.data)
            dev = Developer(cv=cv)
            display_name = form.display_name.data if form.display_name.data != '' \
                else form.user_name.data
            user = User(id=form.user_name.data,
                password=generate_password_hash(form.password.data),
                display_name=display_name, description=form.description.data,
                primary_email=form.email.data, developer=dev)
                #email_addresses=[email], developer=dev)
            db.session.add(user)
            db.session.commit()

            # Generate and send email
            token = generate_confirmation_token(user.primary_email)
            try:
                if app.config['BEHIND_HTTPS_PROXY']:
                    confirm_url = url_for('auth.confirm_email', token=token, \
                        _external=True, _scheme='https')
                else:
                    confirm_url = url_for('auth.confirm_email', token=token, \
                        _external=True)
            except KeyError:
                confirm_url = url_for('auth.confirm_email', token=token, \
                    _external=True)

            html = render_template('email/confirm_user_email.html', \
                confirm_url=confirm_url)
            subject = 'Dreaming Spires email confirmation'
            send_email(user.primary_email, subject, html)

            return render_template('auth/thanks_for_registering.html')
    return render_template('auth/register_developer.html', form=form, \
        entries=list(range(1000)))

@mod_auth.route('/register_client/', methods=['GET', 'POST'])
def register_client():
    return render_template('auth/register_client_temp.html')


#@mod_auth.route('/register_client/', methods=['GET', 'POST'])
def register_client():
    form = RegisterClientForm()
    if form.validate_on_submit():
        if User.query.filter_by(primary_email=form.email.data).first():
            flash('An account has already been registered with this email address.')
        elif User.query.filter_by(id=form.user_name.data).first():
            flash('Username already taken.')
        else:
            display_name = form.display_name.data if form.display_name.data != '' \
                else form.user_name.data
            user = User(id=form.user_name.data,
                password=generate_password_hash(form.password.data),
                display_name=display_name,
                primary_email=form.email.data,
                can_create_departments=True)
            db.session.add(user)
            db.session.commit()

            next = request.args.get('next')
            #if not is_safe_url(next):
            #    return abort(400)
            return redirect(next or url_for('auth.login'))
    return render_template('auth/register_client.html', form=form)

@mod_auth.route('/confirm_email/<token>')
def confirm_email(token):
    try:
        email = confirm_token(token)
    except:
        flash('The confirmation link is invalid or has expired.', 'danger')
    user = User.query.filter_by(primary_email=email).first()

    if not user:
        raise Unauthorized(description='User not tied to a valid email')

    if user.email_verified:
        flash('Email address already confirmed.  Please log in.', 'success')
        return redirect(url_for('auth.login'))
    else:
        user.email_verified = True
        user.date_email_verified = datetime.now()
        db.session.add(user)
        db.session.commit()
        flash('Email address confirmed.  Please log in.', 'success')
        return redirect(url_for('auth.login'))
