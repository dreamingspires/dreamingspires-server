from flask_wtf import FlaskForm # , RecaptchaField
from flask_wtf.file import FileField
from wtforms import validators, StringField, PasswordField, BooleanField, \
    SelectField, RadioField, TextAreaField
from wtforms.widgets import TextInput, TextArea, CheckboxInput, \
    FileInput, HTMLString
from app.static.university_list import university_list

class DatalistInput(TextInput):
    """
    Custom widget to create an input with a datalist attribute
    """

    def __init__(self, placeholder, datalist=""):
        self.placeholder = placeholder
        self.datalist = datalist
        super(DatalistInput, self).__init__()

    def __call__(self, field, **kwargs):
        kwargs.setdefault('id', field.id)
        kwargs.setdefault('name', field.name)

        #field.default - default value which you set in route as form.field.default = ... (at the begin is None)
        #field._value() - value which you get from the form on submit and can use.

        if field.default is None:
            value = ""
        else:
            value = field.default
            
        html = [u'<input class="input" list="{}_list" id="{}" name="{}" value="{}" placeholder="{}">'.
                format(field.id, field.id, field.name, value, self.placeholder),
                u'<datalist class="" id="{}_list">'.format(field.id)]

        for item in field.datalist:
            html.append(u'<option value="{}">'.format(item))
        html.append(u'</datalist>')
        html.append(u'</input>')

        return HTMLString(u''.join(html))

class DatalistField(StringField):
    """
    Custom field type for datalist input
    """

    def __init__(self, placeholder, label=None, datalist="", validators=None, **kwargs):
        self.datalist = datalist
        self.widget = DatalistInput(placeholder, datalist)
        super().__init__(label, validators, **kwargs)

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
                '</p>',
                '</div>']
        return HTMLString(''.join(html))


class PrettyEmailField(StringField):
    """
    Custom field type for email input
    """
    widget = EmailInput()

class PrettyPasswordInput(TextInput):
    def __init__(self, placeholder, *args, **kwargs):
        self.placeholder = placeholder
        super().__init__(*args, **kwargs)
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
                f'<input list="{field.id}" id="{field.id}" name="{field.name}" value="{value}" class="input" type="password" placeholder="{self.placeholder}">',
                '<span class="icon is-small is-left">',
                '<i class="fas fa-lock"></i>',
                '</span>',
                '</p>']
        return HTMLString(''.join(html))

class PrettyPasswordField(PasswordField):
    """
    Custom field type for email input
    """
    def __init__(self, placeholder='Password', *args, **kwargs):
        self.widget = PrettyPasswordInput(placeholder)
        super().__init__(*args, **kwargs)

class PrettyStringInput(TextInput):
    def __init__(self, placeholder, *args, **kwargs):
        self.placeholder = placeholder
        super().__init__(*args, **kwargs)

    def __call__(self, field, **kwargs):
        if field.default is None:
            value = ""
        else:
            value = field.default
        
        html = ['<div class="field">',
                f'<input list="{field.id}" id="{field.id}" name="{field.name}" value="{value}" class="input" type="email" placeholder="{self.placeholder}">',
                '</div>']
        return HTMLString(''.join(html))

class PrettyStringField(PasswordField):
    """
    Custom field type for string input
    """
    def __init__(self, placeholder, *args, **kwargs):
        self.widget = PrettyStringInput(placeholder)
        super().__init__(*args, **kwargs)

class PrettyTextAreaInput(TextArea):
    def __init__(self, placeholder, *args, **kwargs):
        self.placeholder = placeholder
        super().__init__(*args, **kwargs)

    def __call__(self, field, **kwargs):
        if field.default is None:
            value = ""
        else:
            value = field.default
        
        html = ['<div class="field">',
                f'<textarea list="{field.id}" id="{field.id}" name="{field.name}" value="{value}" class="textarea" placeholder="{self.placeholder}"></textarea>'
                '</div>']
        return HTMLString(''.join(html))

class PrettyTextAreaField(TextAreaField):
    """
    Custom field type for string input
    """
    def __init__(self, placeholder, *args, **kwargs):
        self.widget = PrettyTextAreaInput(placeholder)
        super().__init__(*args, **kwargs)

class PrettyBooleanInput(CheckboxInput):
    def __init__(self, text, *args, **kwargs):
        self.text = text
        super().__init__(*args, **kwargs)

    def __call__(self, field, **kwargs):
        if field.default is None:
            value = ""
        else:
            value = field.default

        print(field.render_kw)
        if field.render_kw is None:
            classes = ''
        else:
            classes = ' '.join([f'{k}="{v}"' for k,v in field.render_kw.items()])

        html = ['<div class="field">',
                '<label class="checkbox">',
                f'<input class="checkbox" type="checkbox" list="{field.id}" id="{field.id}" name="{field.name}" value="{value}" {classes}>',
                '&nbsp;' + str(self.text),
                '</input>',
                '</label>',
                '</div>']
        return HTMLString(''.join(html))

class PrettyBooleanField(BooleanField):
    """
    Custom field type for string input
    """
    def __init__(self, text, *args, **kwargs):
        self.widget = PrettyBooleanInput(text)
        super().__init__(*args, **kwargs)

class PrettyFileInput(FileInput):
    def __init__(self, text, *args, **kwargs):
        self.text = text
        super().__init__(*args, **kwargs)

    def __call__(self, field, **kwargs):
        if field.default is None:
            value = ""
        else:
            value = field.default
        
        html = ['<div class="file has-name is-fullwidth">',
                '  <label class="file-label">',
                f'    <input class="file-input" type="file" name="{field.name}" id="{field.id}" value="{value}">',
                '    <span class="file-cta">',
                '      <span class="file-icon">',
                '        <i class="fas fa-upload"></i>',
                '      </span>',
                '      <span class="file-label">',
                str(self.text),
                '      </span>',
                '    </span>',
                '    <span class="file-name">',
                '      File name goes here',
                '    </span>',
                '  </label>',
                '</div>']
        return HTMLString(''.join(html))

class PrettyFileField(FileField):
    """
    Custom field type for string input
    """
    def __init__(self, text, *args, **kwargs):
        self.widget = PrettyFileInput(text)
        super().__init__(*args, **kwargs)

class LoginForm(FlaskForm):
    email    = PrettyEmailField('Email Address', [validators.Email(),
        validators.Required(message='Forgot your email address?')])
    password = PrettyPasswordField('Password', validators=[
        validators.Required(message='Must provide a password. ;-)')])
    remember_me = PrettyBooleanField('Remember me', '')

class RegisterForm(FlaskForm):
    user_name = PrettyStringField('Username', '', validators=[validators.Length(min=3, max=25)])
    email = PrettyEmailField('', [validators.Email(),
        validators.Required(message="Must provide an email address")])
    password = PrettyPasswordField('Password', '', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')])
    confirm = PrettyPasswordField('Repeat Password', '')

    # Optional stuff
    display_name = PrettyStringField('Display Name', '', [validators.Length(max=25)])
    description = PrettyTextAreaField('Describe yourself', '', [validators.Length(max=500)])
    university_check = PrettyBooleanField('I am a university student', '',
            render_kw={'onclick': 'yesnoCheck()'})
    university = DatalistField('Enter your university', '', university_list, default=None)
    upload_cv = PrettyFileField('Choose a file...', 'Upload your CV (optional, .pdf only)', validators=[
            validators.DataRequired()])
    accept_tos = PrettyBooleanField('I accept the Terms of Service', '', [
        validators.DataRequired()])
