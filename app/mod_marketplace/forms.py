from flask_wtf import FlaskForm # , RecaptchaField
from wtforms import validators, StringField, PasswordField, BooleanField, \
    SelectField, RadioField, TextField
from wtforms.fields.html5 import DecimalField
from wtforms.widgets import TextInput, HTMLString
from app.extensions.forms import DatalistField, IconStringField, \
    IconPasswordField, PrettyFileField
