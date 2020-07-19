from flask_wtf import FlaskForm # , RecaptchaField
from flask_wtf.file import FileField
from wtforms import validators, StringField, PasswordField, BooleanField, \
    SelectField, RadioField, TextAreaField, SubmitField
from wtforms.widgets import TextInput, TextArea, CheckboxInput, \
    FileInput, HTMLString, PasswordInput
from app.static.assets.misc.university_list import university_list
from app.extensions.forms import DatalistField, IconStringField, \
    IconPasswordField, PrettyFileField

class LoginForm(FlaskForm):
    email = IconStringField('', validators=[
        validators.Email(), validators.DataRequired()],
        left_logos=['fa-envelope'], render_kw={'placeholder': 'Email'})
    password = IconPasswordField('', validators=[
        validators.DataRequired()],
        render_kw={'placeholder': 'Password'}, left_logos=['fa-lock'])
    remember_me = BooleanField('Remember me', '')
    submit = SubmitField('Log in', render_kw={'class': 'button is-success'})

class RegisterForm(FlaskForm):
    user_name = IconStringField('', 
        validators=[validators.Length(min=3, max=25)],
        render_kw={'placeholder': 'Username'},
        left_logos=['fa-user'])
    email = IconStringField('', [validators.Email(),
        validators.Required(message="Must provide an email address")],
        render_kw={'placeholder': 'Email'}, left_logos=['fa-envelope'])
    password = IconPasswordField('', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')],
        render_kw={'placeholder': 'Password'}, left_logos=['fa-lock'])

    confirm = IconPasswordField('', render_kw={'placeholder': 'Repeat Password'},
        left_logos=['fa-lock'])

    # Optional stuff
    display_name = StringField('', [validators.Length(max=25)],
        render_kw={'placeholder': 'Display Name'})
    description = TextAreaField('', [validators.Length(max=500)],
        render_kw={'placeholder': 'Describe yourself'})
    university_check = BooleanField('I am a university student', \
        render_kw={'onclick': 'yesnoCheck()'})
    university = DatalistField('', \
        university_list, default=None,
        render_kw={'placeholder': 'Enter your university'})
    upload_cv = FileField('Upload your CV (optional, .pdf only)', validators=[
            validators.DataRequired()])
    accept_tos = BooleanField('I accept the Terms of Service', [
        validators.DataRequired()])
    submit = SubmitField('Register', render_kw={'class': 'button is-success'})

#class PrettyRegisterForm(FlaskForm):
#    user_name = StringField('Username', '', validators=[
#        validators.DataRequired(),
#        validators.Length(min=3, max=25)])
#    email = PrettyEmailField('', [validators.Email(),
#        validators.Required(message="Must provide an email address")])
#    password = PrettyPasswordField('Password', '', [
#        validators.DataRequired(),
#        validators.EqualTo('confirm', message='Passwords must match')])
#    confirm = PrettyPasswordField('Repeat Password', '')
#
#    # Optional stuff
#    display_name = PrettyStringField('Display Name', '', [validators.Length(max=25)])
#    description = PrettyTextAreaField('Describe yourself', '', [validators.Length(max=500)])
#    university_check = PrettyBooleanField('I am a university student', '',
#            render_kw={'onclick': 'yesnoCheck()'})
#    university = DatalistField('Enter your university', '', university_list, default=None)
#    upload_cv = PrettyFileField('Choose a file...', 'Upload your CV (optional, .pdf only)', validators=[
#            validators.DataRequired()])
#    accept_tos = PrettyBooleanField('I accept the Terms of Service', '', [
#        validators.DataRequired()])
