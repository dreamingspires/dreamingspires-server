from flask_wtf import FlaskForm # , RecaptchaField
from wtforms import validators, StringField, PasswordField, BooleanField, \
    SelectField, RadioField, FileField
from wtforms.widgets import TextInput, HTMLString
from app.static.university_list import university_list

class DatalistInput(TextInput):
    """
    Custom widget to create an input with a datalist attribute
    """

    def __init__(self, datalist=""):
        super(DatalistInput, self).__init__()
        self.datalist = datalist

    def __call__(self, field, **kwargs):
        kwargs.setdefault('id', field.id)
        kwargs.setdefault('name', field.name)

        #field.default - default value which you set in route as form.field.default = ... (at the begin is None)
        #field._value() - value which you get from the form on submit and can use.

        if field.default is None:
            value = ""
        else:
            value = field.default
            
        html = [u'<input list="{}_list" id="{}", name="{}" value="{}">'.
                format(field.id, field.id, field.name, value), u'<datalist id="{}_list">'.format(field.id)]

        for item in field.datalist:
            html.append(u'<option value="{}">'.format(item))
        html.append(u'</datalist>')

        return HTMLString(u''.join(html))

class DatalistField(StringField):
    """
    Custom field type for datalist input
    """
    widget = DatalistInput()

    def __init__(self, label=None, datalist="", validators=None, **kwargs):
        super(DatalistField, self).__init__(label, validators, **kwargs)
        self.datalist = datalist

    def _value(self):
        if self.data:
            return u''.join(self.data)
        else:
            return u''

class LoginForm(FlaskForm):
    email    = StringField('Email Address', [validators.Email(),
        validators.Required(message='Forgot your email address?')])
    password = PasswordField('Password', [
        validators.Required(message='Must provide a password. ;-)')])

class RegisterForm(FlaskForm):
    username = StringField('Username', [validators.Length(min=3, max=25)])
    email = StringField('Email Address', [validators.Email(),
        validators.Required(message="Must provide an email address")])
    password = PasswordField('New Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField('Repeat Password')
    university_check = BooleanField('I am a university student',
            render_kw={'onclick': 'yesnoCheck()'})
    #university_check = RadioField('', choices=[ \
    #    ('yes', 'I am a university student'), \
    #    ('no', 'I am not a university student')], \
    #    validators=[validators.DataRequired()])
    university = DatalistField('University', university_list, default=None)
    upload_cv = FileField('Upload your CV (.pdf only)', validators=[
        validators.DataRequired(),
        validators.regexp('.+?\.pdf$')])
    accept_tos = BooleanField('I accept the Terms of Service', [
        validators.DataRequired()])
