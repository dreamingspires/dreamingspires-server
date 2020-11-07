from flask_wtf import FlaskForm # , RecaptchaField
from flask_wtf.file import FileField
from wtforms import validators, StringField, PasswordField, BooleanField, \
    SelectField, RadioField, TextAreaField, SubmitField
from wtforms.widgets import TextInput, TextArea, CheckboxInput, \
    FileInput, HTMLString, PasswordInput
from app.static.assets.misc.university_list import university_list
from app.extensions.forms import DatalistField, IconStringField, \
    IconPasswordField, PrettyFileField
import phonenumbers

class LoginForm(FlaskForm):
    email = IconStringField('', validators=[
        validators.Email(), validators.DataRequired()],
        left_logos=['fa-envelope'], render_kw={'placeholder': 'Email'})
    password = IconPasswordField('', validators=[
        validators.DataRequired()],
        render_kw={'placeholder': 'Password'}, left_logos=['fa-lock'])
    remember_me = BooleanField('Remember me', '')
    submit = SubmitField('Log in', render_kw={'class': 'button is-success'})

class RegisterDeveloperForm(FlaskForm):
    user_name = IconStringField('', 
        validators=[validators.Length(min=3, max=25)],
        render_kw={'placeholder': 'Name*'},
        left_logos=['fa-user'])
    email = IconStringField('', [validators.Email(),
        validators.Required(message="Must provide an email address")],
        render_kw={'placeholder': 'Email Address*'}, left_logos=['fa-envelope'])
    # Optional stuff
    phone_number = IconStringField('',
        render_kw={'placeholder': 'Phone Number (Optional)'}, left_logos=['fa-phone'])
    speciality = SelectField('Select Domain Speciality (Optional)', choices=[
        ('None', 'Enter a field'),
        ('Programming', 'Programming'), \
        ('Server-side', 'Server-side'), ('Web Development', 'Web-development')
    ])
    accept_tos = BooleanField('I accept the Terms of Service', [
        validators.DataRequired()])
    submit = SubmitField('Register', render_kw={'class': 'button is-warning is-rounded'})


class RegisterClientForm(FlaskForm):
    user_name = IconStringField('', 
        validators=[validators.Length(min=3, max=25)],
        render_kw={'placeholder': 'Username'},
        left_logos=['fa-user'])
    display_name = StringField('', [validators.Length(max=25)],
        render_kw={'placeholder': 'Display Name'})
    email = IconStringField('', [validators.Email(),
        validators.Required(message="Must provide an email address")],
        render_kw={'placeholder': 'Email'}, left_logos=['fa-envelope'])
    password = IconPasswordField('', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')],
        render_kw={'placeholder': 'Password'}, left_logos=['fa-lock'])
    confirm = IconPasswordField('', render_kw={'placeholder': 'Repeat Password'},
        left_logos=['fa-lock'])
    submit = SubmitField('Register', render_kw={'class': 'button is-success'})

def validate_phone_number(form, number):
    if number.data == '':
        pass
    else:
        try:
            phonenumbers.parse(number.data, 'GB')
        except phonenumbers.phonenumberutil.NumberParseException:
            raise validators.ValidationError('Invalid phone number')

class RegisterClientInterestOld(FlaskForm):
    email = IconStringField('', [validators.Email(),
        validators.Required(message="Must provide an email address")],
        render_kw={'placeholder': 'Email'}, left_logos=['fa-envelope'])
    phone = IconStringField('', [validate_phone_number],
            render_kw={'placeholder': 'Phone number (optional)'},
            left_logos=['fa-phone'])
    organisation = IconStringField('', [],
            render_kw={'placeholder': 'Organisation (optional)'},
            left_logos=['fa-university'])
    estimated_cost = SelectField('Estimated project cost', choices=[
        (None, 'Enter a value'),
        ('<500', '< £500'), ('500-1000', '£500 - £1000'), ('1000-5000', '£1000-5000'), \
        ('5000-10000', '£5000 - £10,000'), ('>10000', '> £10,000')
    ])
    project_description = TextAreaField('', [validators.Length(max=1000)],
        render_kw={'placeholder': 'Describe briefly your project idea'})
    submit = SubmitField('Submit', render_kw={'class': 'button is-success'})

class RegisterClientInterest(FlaskForm):
    name = IconStringField('', [validators.Required(
            message='Must provide a name')],
        render_kw={'placeholder': 'Organisation/University'}, left_logos=['fa-university'])
    organisation = IconStringField('', [validators.Required(
            message='Must provide a name')],
        render_kw={'placeholder': 'Name'}, left_logos=['fa-user'])
    email = IconStringField('', [validators.Email(),
        validators.Required(message="Must provide an email address")],
        render_kw={'placeholder': 'Email'}, left_logos=['fa-envelope'])
    project_description = TextAreaField('', [validators.Required(
            'Must provide a description')],
        render_kw={'placeholder': 'Tell us about your project idea'})
    submit = SubmitField('Submit', render_kw={'class': 
        'button is-warning is-rounded'})
