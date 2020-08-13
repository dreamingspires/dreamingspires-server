# Statement for enabling the development environment
DEBUG = True

# Define the application directory
import os
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
print(f'BASE_DIR: {BASE_DIR}')

# Define the database - we are working with
# SQLite for this example
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'app.db')
DATABASE_CONNECT_OPTIONS = {}

# Additional databases
SQLALCHEMY_BINDS = {
    'mail_db': 'sqlite:///' + os.path.join(BASE_DIR, 'mail.db')
}

# Application threads. A common general assumption is
# using 2 per available processor cores - to handle
# incoming requests using one and performing background
# operations using the other.
THREADS_PER_PAGE = 2

# Enable protection agains *Cross-site Request Forgery (CSRF)*
CSRF_ENABLED     = True

# Use a secure, unique and absolutely secret key for
# signing the data. 
CSRF_SESSION_KEY = "secret"

# Secret key for signing cookies
SECRET_KEY = "secret"
SECURITY_PASSWORD_SALT = 'password_salt'

# Turn off flask-sqlalchemy track modifications (pre-deprecation)
SQLALCHEMY_TRACK_MODIFICATIONS = False

# Configure flask-session
SESSION_TYPE = 'filesystem'

PREFIX='/dreamingspires'
