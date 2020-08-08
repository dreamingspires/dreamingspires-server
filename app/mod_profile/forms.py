from flask_wtf import FlaskForm # , RecaptchaField
from flask_wtf.file import FileField
from wtforms import validators, StringField, PasswordField, BooleanField, \
    SelectField, RadioField, TextAreaField, SubmitField, MultipleFileField
from wtforms.widgets import TextInput, TextArea, CheckboxInput, \
    FileInput, HTMLString, PasswordInput
from app.static.assets.misc.university_list import university_list
from app.extensions.forms import DatalistField, IconStringField, \
    IconPasswordField, PrettyFileField
import app.types as t

def validate_image(form, field):
    if field.data and not str(field.data.filename).endswith(('.jpg', '.png')):
        raise validators.ValidationError('File must be .jpg or .png')

class CreateDepartmentForm(FlaskForm):
    department_name = IconStringField('',
            validators=[validators.Length(min=t.LEN_MIN_UUID, max=t.LEN_UUID)],
            render_kw={'placeholder': 'Department name'},
            left_logos=['fa-university'])
    organisation_name = IconStringField(
            'Your department\'s parent organisation (e.g. university)',
            validators=[validators.Length(min=t.LEN_MIN_UUID, max=t.LEN_UUID)],
            render_kw={'placeholder': 'Organisation Name (Optional)'},
            left_logos=['fa-university'])
    supporting_evidence = MultipleFileField(
        'Upload supporting evidence of your department leadership')
    submit = SubmitField('Submit', render_kw={'class': 'button is-success'})

def generate_edit_user_public_profile_form(user):
    class Form(FlaskForm):
        user_name = IconStringField('', 
            validators=[validators.Length(min=3, max=25)],
            default=user.id,
            render_kw={'disabled': 'disabled'},
            left_logos=['fa-user'])
        email = IconStringField('', [validators.Email(),
            validators.Required(message="Must provide an email address")],
            default=user.primary_email,
            render_kw={'disabled': 'disabled'}, left_logos=['fa-envelope'])
        display_name = StringField('Display Name', [validators.Length(max=25)],
            default=user.display_name)
        description = TextAreaField('Description', [validators.Length(max=500)],
            default=user.description)

        # Optional stuff
        uni_kw = {'onclick': 'yesnoCheck()'}
        if user.educational_institution is not None:
            uni_kw['checked'] = 'checked'
        university_check = BooleanField('I am a university student',
            render_kw=uni_kw)
        university = DatalistField('Enter your university',
            university_list,
            default=user.educational_institution \
                if user.educational_institution is not None else '')
        display_image = FileField('Change profile picture',
            [validate_image])

        #password = IconPasswordField('', [
        #    validators.DataRequired(),
        #    validators.EqualTo('confirm', message='Passwords must match')],
        #    render_kw={'placeholder': 'Password'}, left_logos=['fa-lock'])

        #confirm = IconPasswordField('', render_kw={'placeholder': 'Repeat Password'},
        #    left_logos=['fa-lock'])
    return Form()
