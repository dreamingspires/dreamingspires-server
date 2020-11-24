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
from flask_admin import Admin
from werkzeug.exceptions import HTTPException
from werkzeug.utils import ImportStringError

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
try:
    app.config.from_object('secret_config')
except ImportStringError:
    print('Warning: secret_config.py not found')

# Add the fathom analytics ID
@app.context_processor
def inject_id():
    if 'FATHOM_ID' in app.config.keys():
        return dict(FATHOM_ID=app.config['FATHOM_ID'])

    return {}

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
admin = Admin(app, name='Dreaming Spires Admin', template_mode='bootstrap3')

# Define the back-end file storage
try:
    default_storage = app.config['DEFAULT_STORAGE']
except KeyError:
    default_storage = {'depot.storage_path': '/tmp/depot/'}
try:
    image_storage = app.config['IMAGE_STORAGE']
except KeyError:
    image_storage = {'depot.storage_path': '/tmp/depot_images/'}
try:
    blog_image_storage = app.config['BLOG_IMAGE_STORAGE']
except KeyError:
    blog_image_storage = {'depot.storage_path': '/tmp/depot_blog_images/'}

DepotManager.configure('default', default_storage)
DepotManager.configure('images', image_storage)
DepotManager.configure('blog_images', blog_image_storage)

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

try:
    if app.config['PREFIX']:
        app.wsgi_app = PrefixMiddleware(app.wsgi_app, prefix=app.config['PREFIX'])
except KeyError:
    pass


nav.Bar('end', [
    nav.Item('Home', 'index'),
    nav.Item('Our Services', 'our_services'),
    nav.Item('Portfolio', 'portfolio'),
    nav.Item('Develop with Us', 'develop_with_us'),
    nav.Item('Log in', 'auth.login')
])

nav.Bar('buttons', [
    nav.Item('Contact Us', 'contact'),
])

#nav.Bar('login', [
#    nav.Item('Log in', 'auth.login')
#])

nav.Bar('footer', [
    nav.Item('Home', 'index'),
    nav.Item('About', 'index', args={'_anchor':'page_1'}),
    nav.Item('Developer FAQ', 'developer_faq'),
    nav.Item('Client FAQ', 'client_faq'),
    nav.Item('Contact', 'contact'),
    nav.Item('Privacy Policy', 'privacy_policy'),
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

# Register admin interface
print('before importing admin')
from app import admin_interface
print('done importing admin')

# Build the database:
# This will create the database files using SQLAlchemy
db.create_all()

# Register admin users
from app.models import User, Developer
from werkzeug.security import generate_password_hash
from datetime import datetime
try:
    app.config['ADMIN_USERS']
except KeyError:
    pass
else:
    for (username, password, email) in app.config['ADMIN_USERS']:
        if not User.query.filter_by(id=username).first():
            user = User(id=username,
                password=generate_password_hash(password),
                display_name='', description='',
                primary_email=email, is_admin=True,
                email_verified=True, date_email_verified=datetime.now())
            db.session.add(user)
    db.session.commit()

# Permit sqlite downgrades
with app.app_context():
    if db.engine.url.drivername == 'sqlite':
        migrate.init_app(app, db, render_as_batch=True)
    else:
        migrate.init_app(app, db)
