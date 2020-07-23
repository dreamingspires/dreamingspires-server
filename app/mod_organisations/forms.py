from flask_wtf import FlaskForm # , RecaptchaField
from wtforms import validators, StringField, PasswordField, BooleanField, \
    SelectField, RadioField, TextField, TextAreaField, SubmitField
from wtforms.fields.html5 import DecimalField
from wtforms.widgets import TextInput, HTMLString
from app.extensions.forms import DatalistField, IconStringField, \
    IconPasswordField, PrettyFileField

class CreateProjectForm(FlaskForm):
    display_name = IconStringField('', validators=[
        validators.DataRequired()], render_kw={'placeholder': 'Project Name'})
    description = TextAreaField('', [validators.Length(max=500)],
        render_kw={'placeholder': 'Describe your project'})
    price = DecimalField('', validators=[
            validators.NumberRange(min=0)], # TODO: write custom validator
        render_kw={'step': '.01', 'min': 0, 'placeholder': 'Enter a price'})
    submit = SubmitField('Create', render_kw={'class': 'button is-success'})
