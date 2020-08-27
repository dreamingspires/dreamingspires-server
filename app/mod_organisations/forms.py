from flask_wtf import FlaskForm # , RecaptchaField
from flask_wtf.file import FileField
from wtforms import validators, StringField, PasswordField, BooleanField, \
    SelectField, RadioField, TextField, TextAreaField, SubmitField, \
    MultipleFileField
from wtforms.fields.html5 import DecimalField
from wtforms.widgets import TextInput, HTMLString
from app.extensions.forms import DatalistField, IconStringField, \
    IconPasswordField, PrettyFileField
from app.extensions.forms import validate_image

class CreateProjectForm(FlaskForm):
    display_name = IconStringField('', validators=[
        validators.DataRequired()], render_kw={'placeholder': 'Project Name'})
    description = TextAreaField('', [validators.Length(max=500)],
        render_kw={'placeholder': 'Describe your project'})
    price = DecimalField('', validators=[
            validators.NumberRange(min=0)], # TODO: write custom validator
        render_kw={'step': '.01', 'min': 0, 'placeholder': 'Enter a price'})
    submit = SubmitField('Create', render_kw={'class': 'button is-success'})

def generate_edit_organisation_form(dep):
    try:
        organisation_name = dep.organisation.display_name
    except AttributeError:
        organisation_name = dep.temp_organisation

    class Form(FlaskForm):
        organisation = IconStringField('', 
            validators=[validators.Length(min=3, max=25)],
            default=organisation_name,
            render_kw={'disabled': 'disabled'},
            left_logos=['fa-university'])
        display_name = StringField('', [validators.Length(max=25)],
            default=dep.display_name,
            render_kw={'disabled': 'disabled'})

        description = TextAreaField('Description', [validators.Length(max=500)],
            default=dep.description)
        display_image = FileField('Change profile picture',
            [validate_image])
        # This only displayed while the application is pending
        supporting_evidence = MultipleFileField('')
        # TODO: Extra supporting evidence
        submit = SubmitField('Save changes', render_kw={'class': 'button is-success'})


    return Form()
