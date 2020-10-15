# TODO: clean up unused dependencies
from flask_wtf import FlaskForm # , RecaptchaField
from flask_wtf.file import FileField
from wtforms import validators, StringField, PasswordField, BooleanField, \
    SelectField, RadioField, TextAreaField, SubmitField
from wtforms.widgets import TextInput, TextArea, CheckboxInput, \
    FileInput, HTMLString, PasswordInput
from app.static.assets.misc.university_list import university_list
from app.extensions.forms import DatalistField, IconStringField, \
    IconPasswordField, PrettyFileField, IconTextAreaField

class RegisterClientInterest(FlaskForm):
    name = IconStringField('', [validators.Required(
            message='Must provide a name')],
        render_kw={'placeholder': 'Name'}, left_logos=['fa-user'])
    email = IconStringField('', [validators.Email(),
        validators.Required(message="Must provide an email address")],
        render_kw={'placeholder': 'Email'}, left_logos=['fa-envelope'])
    organisation = IconStringField('', [validators.Required(
            message='Must provide an organisation')],
        render_kw={'placeholder': 'Organisation/University'}, left_logos=['fa-university'])
    # Use logo lightbulb
    project_description = IconTextAreaField('', [validators.Required(
            'Must provide a description')],
        render_kw={'placeholder': 'Tell us about your project idea',
            'style': 'height: 250px'}, left_logos=['fa-lightbulb'])
    submit = SubmitField('Submit', render_kw={'class': 
        'button is-warning is-rounded'})
