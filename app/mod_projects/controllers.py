# Import flask dependencies
from flask import Blueprint, request, render_template, \
                  flash, g, session, redirect, url_for

# Import password / encryption helper tools
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug import secure_filename

# Import the database object from the main app module
from app import db

# Import module forms
from app.mod_auth.forms import LoginForm, RegisterForm

# Import module models (i.e. User)
from app.mod_auth.models import User, Email, Matrix, CV, Developer, \
    Organisation, Project

# Define the blueprint: 'auth', set its url prefix: app.url/auth
mod_auth = Blueprint('auth', __name__, url_prefix='/auth')


@mod_auth.route('/projects/', methods=['GET', 'POST'])
def projects():
    # Ensure the user is logged in
    assert

@mod_auth.route('/home/', methods=['GET', 'POST'])
def home():
    return 'Successfully logged in'

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
            session['user_id'] = user.id
            session['logged_in'] = True
            return redirect(url_for('auth.home'))

        flash('Wrong email or password', 'error-message')

    return render_template('auth/signin.html', form=form)

@mod_auth.route('/register/', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        # Check username is not already taken
        if User.query.filter_by(primary_email=form.email.data).first():
            flash('An account has already been registered with this email address.')
        elif User.query.filter_by(user_name=form.user_name.data).first():
            flash('Username already taken.')
        else:
            cv = CV(document=form.upload_cv.data)
            dev = Developer(cv=cv)
            display_name2 = form.display_name.data if form.display_name.data != '' \
                else form.user_name.data
            user = User(user_name=form.user_name.data,
                password=generate_password_hash(form.password.data),
                display_name=display_name2, description=form.description.data,
                primary_email=form.email.data, developer=dev)
                #email_addresses=[email], developer=dev)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form, entries=list(range(1000)))
