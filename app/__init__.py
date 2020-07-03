from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_navigation import Navigation
from depot.manager import DepotManager
from flask_login import LoginManager
from flask_principal import Principal

from app.utils import register_template_utils 

# Define the back-end file storage
DepotManager.configure('default', {'depot.storage_path': '/tmp/depot/'})

# Define the WSGI application object
app = Flask(__name__)

# Configurations
app.config.from_object('config')

# Define the database object which is imported
# by modules and controllers
db = SQLAlchemy(app)
nav = Navigation(app)
login_manager = LoginManager(app)
principals = Principal(app)
register_template_utils(app)

# login_manager settings
from app.mod_auth.models import User
@login_manager.user_loader
def load_user(uid):
    return User.query.filter_by(id=uid).first()
login_manager.login_view = 'auth.login'


nav.Bar('top', [
    nav.Item('Home', 'index'),
    nav.Item('<strong>Sign up</strong>', 'auth.register'),
    nav.Item('Log in', 'auth.login')
])

# Import views
from app import views

# Sample HTTP error handling
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

# Import a module / component using its blueprint handler variable (mod_auth)
from app.mod_auth.controllers import mod_auth as auth_module
from app.mod_profile.controllers import mod_profile as profile_module

# Register blueprint
app.register_blueprint(auth_module)
app.register_blueprint(profile_module)

# Build the database:
# This will create the database file using SQLAlchemy
db.create_all()
