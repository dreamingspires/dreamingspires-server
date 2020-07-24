from flask_wtf import FlaskForm # , RecaptchaField
from wtforms import validators, StringField, PasswordField, BooleanField, \
    SelectField, RadioField, TextField, TextAreaField, SubmitField
from wtforms.fields.html5 import DecimalField
from wtforms.fields import HiddenField
from wtforms.widgets import TextInput, HTMLString
from app.extensions.forms import DatalistField, IconStringField, \
    IconPasswordField, PrettyFileField

class ReplyForm(FlaskForm):
    comment = TextAreaField('', [validators.Length(max=500)],
        render_kw={'placeholder': 'Add a comment...', 'class': 'textarea'})

#    def __init__(self, reply_code, *args, **kwargs):
#        super().__init__(*args, **kwargs)
#        self.reply_code = self._fields['reply_code'] = self.meta.bind_field(
#            self, HiddenField(reply_code),
#            {'name': 'reply_code', 'prefix': self._prefix})

def generate_reply_form(reply_code, is_reply=False):
    class SubReplyForm(ReplyForm):
        pass
    SubReplyForm.reply_code = HiddenField(render_kw={'value': reply_code})
    if is_reply:
        SubReplyForm.submit = SubmitField('Post reply',
            render_kw={'class': 'button is-success'})
    else:
        SubReplyForm.submit = SubmitField('Post comment',
            render_kw={'class': 'button is-success'})

    return SubReplyForm()


class Chat():
    def __init__(self, children):
        self.children = children

    def render(self):
        lines = [child.render() for child in self.children]
        return '\n'.join(lines)


class ChatComment():
    def __init__(self, profile_name, profile_image, comment_time, \
            comment_text, comment_id, is_sub_comment=False, children=[]):
        self.profile_name = profile_name
        if profile_image is None:
            self.profile_image = 'https://bulma.io/images/placeholders/128x128.png'
        else:
            self.profile_image = profile_image
        self.comment_time = comment_time
        self.comment_text = comment_text
        self.comment_id = comment_id
        self.is_sub_comment = is_sub_comment
        self.children = children

    def render(self):
        picture_size = 'is-48x48' if self.is_sub_comment else 'is-64x64'
        if self.is_sub_comment:
            response_bar = '<small><a>Like</a> · {}</small>'.format(self.comment_time)
        else:
            collapsible_id = f'{self.comment_id}_collapsible'
            response_bar = f'<small><a>Like</a> · <a href="#{collapsible_id}" data-action="collapse">Reply</a> · {self.comment_time}</small>'
            chat_reply = ChatReply(f'{self.comment_id}_reply', is_reply=True)

        lines = ["""
            <article class="media">
              <figure class="media-left">
                <p class="image {}">
                  <img src="{}" style="border-radius:10%">
                </p>
              </figure>
              <div class="media-content">
                <div class="content">
                  <p>
                    <strong>{}</strong>
                    <br>
                        {}
                    <br>
                    {}
                  </p>
                </div>
        """.format(picture_size, self.profile_image, self.profile_name, \
                self.comment_text, response_bar)]
        for child in self.children:
            lines.append(child.render())
        # Render the reply box
        if not self.is_sub_comment:
            lines.append(f'<div id="{collapsible_id}" class="is-collapsible">')
            lines.append(chat_reply.render())
            lines.append('</div>')
        lines.append('</div>')
        lines.append('</article>')

        return '\n'.join(lines)


class ChatReply():
    def __init__(self, reply_code, is_reply=False, collapsible_id=None):
        self.form = generate_reply_form(reply_code, is_reply=is_reply)
    
    def render(self):
        return """
            <article class="media">
              <figure class="media-left">
                <p class="image is-64x64">
                  <img src="https://bulma.io/images/placeholders/128x128.png">
                </p>
              </figure>
              <div class="media-content">
                <form method="post" action="." role="form" accept-charset="UTF-8" enctype="multipart/form-data" novalidate>
                {}
                <div class="field">
                  <p class="control">
                    {}
                  </p>
                </div>
                <div class="field">
                  <p class="control">
                    {}
                  </p>
                </div>
              </div>
            </article>
        """.format(self.form.reply_code(), self.form.comment(), self.form.submit())
        # self.form.hidden_tag()
