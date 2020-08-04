from flask_wtf import FlaskForm
from wtforms import validators, TextAreaField, SubmitField
from wtforms.fields import HiddenField

class ReplyForm(FlaskForm):
    reply_code = HiddenField(render_kw={'value': 'base'})
    body = TextAreaField('', [validators.Length(max=500, min=1)],
        render_kw={'placeholder': 'Add a comment...', 'class': 'textarea'})
    submit = SubmitField('Submit', render_kw={'class': 'button is-success'})
