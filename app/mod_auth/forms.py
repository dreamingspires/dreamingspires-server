from flask_wtf import FlaskForm # , RecaptchaField
from flask_wtf.file import FileField
from wtforms import validators, StringField, PasswordField, BooleanField, \
    SelectField, RadioField, TextField
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

        return htmlstring(u''.join(html))

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

class EmailInput(TextInput):
    """
    Custom widget to create an email input box
    Depends upon the bulma CSS framework
    """
    def __call__(self, field, **kwargs):
        if field.default is None:
            value = ""
        else:
            value = field.default
        
        html = ['<div class="field">',
                '<p class="control has-icons-left has-icons-right">',
                f'<input list="{field.id}" id="{field.id}" name="{field.name}" value="{value}" class="input" type="email" placeholder="Email">',
                '<span class="icon is-small is-left">',
                '<i class="fas fa-envelope"></i>',
                '</span>',
                '<span class="icon is-small is-right">',
                '<i class="fas fa-check"></i>',
                '</span>',
                '</p>']
        return HTMLString(''.join(html))

class PrettyEmailField(StringField):
    """
    Custom field type for email input
    """
    widget = EmailInput()

class PasswordInput(TextInput):
    """
    Custom widget to create a password input box
    Depends upon the bulma CSS framework
    """
    def __call__(self, field, **kwargs):
        if field.default is None:
            value = ""
        else:
            value = field.default
        
        html = ['<div class="field">',
                '<p class="control has-icons-left has-icons-right">',
                f'<input list="{field.id}" id="{field.id}" name="{field.name}" value="{value}" class="input" type="password" placeholder="Password">',
                '<span class="icon is-small is-left">',
                '<i class="fas fa-lock"></i>',
                '</span>',
                '</p>']
        return HTMLString(''.join(html))

class PrettyPasswordField(PasswordField):
    """
    Custom field type for email input
    """
    widget = PasswordInput()

class LoginForm(FlaskForm):
    email    = PrettyEmailField('Email Address', [validators.Email(),
        validators.Required(message='Forgot your email address?')])
    password = PrettyPasswordField('Password', [
        validators.Required(message='Must provide a password. ;-)')])
    remember_me = BooleanField('Remember me')

class RegisterForm(FlaskForm):
    user_name = StringField('Username', [validators.Length(min=3, max=25)])
    email = PrettyEmailField('Email Address', [validators.Email(),
        validators.Required(message="Must provide an email address")])
    password = PrettyPasswordField('New Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')])
    confirm = PrettyPasswordField('Repeat Password')

    # Optional stuff
    display_name = StringField('Display Name', [validators.Length(max=25)])
    description = TextField('Describe yourself', [validators.Length(max=500)])
    university_check = BooleanField('I am a university student',
            render_kw={'onclick': 'yesnoCheck()'})
    university = DatalistField('University', university_list, default=None)
    upload_cv = FileField('Upload your CV (.pdf only)')
    accept_tos = BooleanField('I accept the Terms of Service', [
        validators.DataRequired()])
