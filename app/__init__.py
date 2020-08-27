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
from flask_mail import Mail
from werkzeug.exceptions import HTTPException

from app.utils import register_template_utils 

class PrefixMiddleware(object):
    def __init__(self, app, prefix=''):
        self.app = app
        self.prefix = prefix

    def __call__(self, environ, start_response):

        if environ['PATH_INFO'].startswith(self.prefix):
            environ['PATH_INFO'] = environ['PATH_INFO'][len(self.prefix):]
            environ['SCRIPT_NAME'] = self.prefix
            return self.app(environ, start_response)
        else:
            start_response('404', [('Content-Type', 'text/plain')])
            return ["This url does not belong to the app.".encode()]

# Define the WSGI application object
app = Flask(__name__)

# Set jinja2 settings
app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True

# Configurations
app.config.from_object('config')
app.config.from_object('secret_config')

# Register extensions with app
db = SQLAlchemy(app)
nav = Navigation(app)
login_manager = LoginManager(app)
principals = Principal(app)
register_template_utils(app)
Session(app)
#socketio = SocketIO(app, manage_session=False, path='dreamingspires/socket.io')
socketio = SocketIO(app, manage_session=False)
        # Sessions are managed with flask-session
migrate = Migrate(app, db)
mail = Mail(app)

# Define the back-end file storage
DepotManager.configure('default', {'depot.storage_path': '/tmp/depot/'})
DepotManager.configure('images', {'depot.storage_path': '/tmp/depot_images/'})
#if app.config['PREFIX']:
#    app.wsgi_app = DepotManager.make_middleware(app.wsgi_app, \
#        mountpoint=app.config['PREFIX'])
#else:
app.wsgi_app = DepotManager.make_middleware(app.wsgi_app)

# login_manager settings
from app.models import User
@login_manager.user_loader
def load_user(uid):
    return User.query.filter_by(id=uid).first()
login_manager.login_view = 'auth.login'

#try:
if app.config['PREFIX']:
    app.wsgi_app = PrefixMiddleware(app.wsgi_app, prefix=app.config['PREFIX'])
#except KeyError:
#    pass


nav.Bar('start', [
    nav.Item('Home', 'index'),
    nav.Item('About', 'index', args={'_anchor':'about'}),
    nav.Item('Contact', 'contact'),
])

nav.Bar('end', [
    nav.Item('<strong>Sign up</strong>', 'auth.register_developer'),
    nav.Item('Log in', 'auth.login')
])

nav.Bar('footer', [
    nav.Item('Home', 'index'),
    nav.Item('About', 'index', args={'_anchor':'about'}),
    nav.Item('Developer FAQ', 'developer_faq'),
    nav.Item('Client FAQ', 'client_faq'),
    nav.Item('Contact', 'contact'),
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
@app.errorhandler(HTTPException)
def not_found(error):
    split_errors = [s.strip() for s in str(error).split(':')]
    return render_template('error.html', heading=split_errors[0], errors=split_errors[1:])

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
