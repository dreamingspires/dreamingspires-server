from flask import Flask, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_navigation import Navigation
from depot.manager import DepotManager
from flask_login import LoginManager
from flask_principal import Principal
from flask_socketio import SocketIO
from flask_session import Session   # Required because socketio can't modify
                                    # default cookie-based sessions
from flask_migrate import Migrate

from app.utils import register_template_utils 

# Define the WSGI application object
app = Flask(__name__)

# Set jinja2 settings
app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True

# Configurations
app.config.from_object('config')

# Register extensions with app
db = SQLAlchemy(app)
nav = Navigation(app)
login_manager = LoginManager(app)
principals = Principal(app)
register_template_utils(app)
Session(app)
socketio = SocketIO(app, manage_session=False)
        # Sessions are managed with flask-session
migrate = Migrate(app, db)

# Define the back-end file storage
DepotManager.configure('default', {'depot.storage_path': '/tmp/depot/'})
DepotManager.configure('images', {'depot.storage_path': '/tmp/depot_images/'})
app.wsgi_app = DepotManager.make_middleware(app.wsgi_app)

# login_manager settings
from app.models import User
@login_manager.user_loader
def load_user(uid):
    return User.query.filter_by(id=uid).first()
login_manager.login_view = 'auth.login'


nav.Bar('start', [
    nav.Item('Home', 'index'),
    nav.Item('About', 'index', args={'_anchor':'about'}),
    nav.Item('Contact', 'contact', args={'_anchor':'contact'}),
])

nav.Bar('end', [
    nav.Item('<strong>Sign up</strong>', 'auth.register_developer'),
    nav.Item('Log in', 'auth.login')
])

nav.Bar('profile', [
    nav.Item('Inbox', 'mail.inbox'),
    nav.Item('Edit profile', 'profile.edit_profile'),
    nav.Item('Marketplace', 'marketplace.marketplace'),
    nav.Item('Log out', 'auth.logout')
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
from app.mod_marketplace.controllers import mod_marketplace as marketplace_module
from app.mod_organisations.controllers import mod_organisations \
    as organisations_module
from app.mod_mail.controllers import mod_mail as mail_module

# Register blueprint
app.register_blueprint(auth_module)
app.register_blueprint(profile_module)
app.register_blueprint(marketplace_module)
app.register_blueprint(organisations_module)
app.register_blueprint(mail_module)

# Build the database:
# This will create the database files using SQLAlchemy
db.create_all()
