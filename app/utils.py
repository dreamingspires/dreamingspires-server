# https://github.com/hack4impact/flask-base/blob/master/app/utils.py

def register_template_utils(app):
    @app.template_global()
    def is_hidden_field(field):
        from wtforms.fields import HiddenField
        return isinstance(field, HiddenField)
