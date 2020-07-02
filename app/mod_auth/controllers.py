# Import flask dependencies
from flask import Blueprint, request, render_template, \
                  flash, g, session, redirect, url_for

# Import password / encryption helper tools
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug import secure_filename

# Import the database object from the main app module
from app import db

# Import module forms
from app.mod_auth.forms import LoginForm, RegisterForm, CVForm

# Import module models (i.e. User)
from app.mod_auth.models import User, Email, Matrix, CV, Developer, \
    Organisation, Project

# Define the blueprint: 'auth', set its url prefix: app.url/auth
mod_auth = Blueprint('auth', __name__, url_prefix='/auth')

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
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            session['user_id'] = user.id
            flash('Welcome %s' % user.name)
            return redirect(url_for('auth.home'))

        flash('Wrong email or password', 'error-message')

    return render_template('auth/signin.html', form=form)

@mod_auth.route('/register/', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    print(form.errors)
    if form.validate_on_submit():
        print('form validated')
        print(form.upload_cv.data)
        #f = form.upload_cv.data
        #filename = secure_filename(f.filename)

        #cv = CV(document=b'test document')
        cv = CV(document=form.upload_cv.data)
        dev = Developer(display_name=form.display_name.data, cv=cv)
        email = Email(email=form.email.data)
        user = User(user_name=form.user_name.data,
                    password=generate_password_hash(form.password.data),
                    developer=dev)
                    #email_addresses=[email], developer=dev)
        user.email_addresses.append(email)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form, entries=list(range(1000)))
