from wtforms import validators, StringField, PasswordField, FileField
from wtforms.widgets import TextInput, FileInput, PasswordInput, HTMLString

def validate_image(form, field):
    if field.data and not str(field.data.filename).endswith(
            ('.jpg', '.JPG', '.jpeg', '.JPEG', '.png', '.PNG')):
        raise validators.ValidationError('File must be .jpg or .png')

class DatalistInput(TextInput):
    """
    Custom widget to create an input with a datalist attribute
    """

    def __init__(self, datalist=""):
        self.datalist = datalist
        super().__init__()

    def __call__(self, field, **kwargs):
        id=f'{field.id}_list'
        kwargs['list'] = f'{id}'
        
        super_html = super().__call__(field, **kwargs)
        kwargs.setdefault('id', field.id)
        kwargs.setdefault('name', field.name)

        #field.default - default value which you set in route as form.field.default = ... (at the begin is None)
        #field._value() - value which you get from the form on submit and can use.

        if field.default is None:
            value = ""
        else:
            value = field.default

        html = [super_html,
                f'<datalist class="" id="{id}">']
        for item in field.datalist:
            html.append(u'<option value="{}">'.format(item))
        html.append(u'</datalist>')

        return HTMLString(u''.join(html))

class DatalistField(StringField):
    """
    Custom field type for datalist input
    """

    def __init__(self, label=None, datalist="", validators=None, **kwargs):
        self.datalist = datalist
        self.widget = DatalistInput(datalist)
        super().__init__(label, validators, **kwargs)

    def _value(self):
        if self.data:
            return u''.join(self.data)
        else:
            return u''

class IconTextInput(TextInput):
    """
    Custom widget to create an input box that displays logos
    """

    def __init__(self, left_logos, right_logos):
        self.where_has_icons = ''
        if left_logos is None:
            self.left_logos = None
        else:
            self.left_logos = ' '.join(left_logos)
            self.where_has_icons += ' has-icons-left'
        if right_logos is None:
            self.right_logos = None
        else:
            self.right_logos = ' '.join(right_logos)
            self.where_has_icons += ' has-icons-right'

    def __call__(self, field, **kwargs):
        if field.default is None:
            value = ""
        else:
            value = field.default

        html = [f'<div class="control {self.where_has_icons}">',
                super().__call__(field, **kwargs)]
        if self.left_logos is not None:
            html.extend(['<span class="icon is-small is-left">',
                         f'<i class="fas {self.left_logos}"></i>',
                         '</span>'])
        if self.right_logos is not None:
            html.extend(['<span class="icon is-small is-right">',
                         f'<i class="fas {self.right_logos}"></i>',
                         '</span>'])
        html.append('</div>')
        return HTMLString(''.join(html))

class IconStringField(StringField):
    """
    Custom field type to create an input box that displays logos
    """

    def __init__(self, label=None, validators=None, \
            left_logos=None, right_logos=None, **kwargs):
        self.widget = IconTextInput(left_logos, right_logos)
        super().__init__(label, validators, **kwargs)

class IconPasswordInput(PasswordInput):
    """
    Custom widget to create a password box that displays logos
    """

    def __init__(self, left_logos, right_logos, hide_value=True):
        self.where_has_icons = ''
        if left_logos is None:
            self.left_logos = None
        else:
            self.left_logos = ' '.join(left_logos)
            self.where_has_icons += ' has-icons-left'
        if right_logos is None:
            self.right_logos = None
        else:
            self.right_logos = ' '.join(right_logos)
            self.where_has_icons += ' has-icons-right'
        self.hide_value = hide_value

    def __call__(self, field, **kwargs):
        if field.default is None:
            value = ""
        else:
            value = field.default

        html = [f'<div class="control {self.where_has_icons}">',
                super().__call__(field, **kwargs)]
        if self.left_logos is not None:
            html.extend(['<span class="icon is-small is-left">',
                         f'<i class="fas {self.left_logos}"></i>',
                         '</span>'])
        if self.right_logos is not None:
            html.extend(['<span class="icon is-small is-right">',
                         f'<i class="fas {self.right_logos}"></i>',
                         '</span>'])
        html.append('</div>')
        return HTMLString(''.join(html))

class IconPasswordField(PasswordField):
    """
    Custom field type to create a password box that displays logos
    """

    def __init__(self, label=None, validators=None, \
            left_logos=None, right_logos=None, **kwargs):
        self.widget = IconPasswordInput(left_logos, right_logos)
        super().__init__(label, validators, **kwargs)

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
