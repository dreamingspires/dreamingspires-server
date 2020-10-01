# Defines the admin panel
from flask_login import current_user
from flask_admin.contrib.sqla import ModelView
from app.models import User, CV, Developer, Organisation, Department, \
    DepartmentFile, DeveloperProjectsMap, Project, ProjectTag, BlogPost, BlogImage
import PIL
from flask_wtf.file import FileField

from app.extensions.forms import validate_image
from app import admin, db

class AdminView(ModelView):
    def is_accessible(self):
        try:
            print(f'is_authenticated: {current_user.is_authenticated}')
            print(f'is_admin: {current_user.is_admin}')
            return current_user.is_authenticated and current_user.is_admin
        except AttributeError:
            # In case the user hasn't been initialised, so is_admin doesn't
            # exist (because not in AnonymousUserMixin)
            return False

class BaseView(AdminView):
    form_excluded_columns=['date_created', 'date_modified']

class ImageView(BaseView):
    form_extra_fields = {'display_image2': FileField('Display Image', [validate_image])}

    def on_model_change(self, form, Object, is_created):
        if form.display_image2.data:
            try:
                Object.display_image = form.display_image2.data
            except PIL.UnidentifiedImageError:
                raise UnsupportedMediaType( \
                    description="Uploaded file is not an image")

class BlogPostView(AdminView):
    form_extra_fields = {'display_image2': FileField('Display Image', [validate_image]),
        'portfolio_image2': FileField('Portfolio Image', [validate_image])}

    def on_model_change(self, form, Object, is_created):
        if form.display_image2.data:
            try:
                Object.display_image = form.display_image2.data
            except PIL.UnidentifiedImageError:
                raise UnsupportedMediaType( \
                    description="Uploaded file is not an image")

        if form.portfolio_image2.data:
            try:
                Object.portfolio_image = form.portfolio_image2.data
            except PIL.UnidentifiedImageError:
                raise UnsupportedMediaType( \
                    description="Uploaded file is not an image")

class BlogImageView(ImageView):
    column_formatters = dict(url=lambda v, c, m, p: m.display_image.url)

    def get_column_names(self, only_columns, excluded_columns):
        only_columns.append('url')
        return super().get_column_names(only_columns, excluded_columns)


admin.add_view(BaseView(User, db.session))
admin.add_view(BaseView(CV, db.session))
admin.add_view(BaseView(Developer, db.session))
admin.add_view(BaseView(Organisation, db.session))
admin.add_view(BaseView(Department, db.session))
admin.add_view(BaseView(DepartmentFile, db.session))
admin.add_view(BaseView(DeveloperProjectsMap, db.session))
admin.add_view(BaseView(Project, db.session))
admin.add_view(BaseView(ProjectTag, db.session))
admin.add_view(BlogPostView(BlogPost, db.session))
admin.add_view(BlogImageView(BlogImage, db.session))
