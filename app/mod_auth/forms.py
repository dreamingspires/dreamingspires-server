from flask_wtf import FlaskForm # , RecaptchaField
from wtforms import validators, StringField, PasswordField, BooleanField

class LoginForm(FlaskForm):
    email    = StringField('Email Address', [validators.Email(),
        validators.Required(message='Forgot your email address?')])
    password = PasswordField('Password', [
        validators.Required(message='Must provide a password. ;-)')])

class RegisterForm(FlaskForm):
    username = StringField('Username', [validators.Length(min=4, max=25)])
    email = StringField('Email Address', [validators.Email(),
        validators.Required(message="Must provide an email address")])
    password = PasswordField('New Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField('Repeat Password')
    accept_tos = BooleanField('I accept the Terms of Service', [
        validators.DataRequired()])

