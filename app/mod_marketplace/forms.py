from flask_wtf import FlaskForm # , RecaptchaField
from wtforms import validators, StringField, PasswordField, BooleanField, \
    SelectField, RadioField, TextField, TextAreaField
from wtforms.fields.html5 import DecimalField
from wtforms.fields import HiddenField
from wtforms.widgets import TextInput, HTMLString
from app.extensions.forms import DatalistField, IconStringField, \
    IconPasswordField, PrettyFileField

class CommentForm(FlaskForm):
    def __init__(self, reply_code):
        self.reply_code = HiddenField(reply_code)
        self.comment = TextAreaField('', [validators.Length(max=500)],
            render_kw={'placeholder': 'Add a comment...'}
        self.submit = SubmitField('Post comment', 
            render_kw={'class': 'button is-success'})
