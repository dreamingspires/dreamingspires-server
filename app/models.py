# Defines the database schemata used throughout the site
# Could maybe be separated into the separate blueprints, but all the
# tables are interdependent (such as Developers being linked to Users and
# Projects), so for now all the databases are defined here instead

from app import db
import app.types as t
from depot.fields.sqlalchemy import UploadedFileField
from depot.fields.specialized.image import UploadedImageWithThumb
from flask_login import UserMixin
import uuid

from colour import Color
from sqlalchemy_utils import ColorType
from sqlalchemy.types import Text

# Define a base model for other database tables to inherit
class Base(db.Model):
    __abstract__  = True
    id = db.Column(db.String(t.LEN_UUID), primary_key=True, default=lambda:uuid.uuid4().hex)
    date_created = db.Column(db.DateTime,  default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime,  default=db.func.current_timestamp(),
                                           onupdate=db.func.current_timestamp())
class BaseRequiresVerification(Base):
    __abstract__  = True
    verification_status = db.Column(db.Enum(t.VerificationStatus), \
        nullable=False, default=t.VerificationStatus.not_submitted)
    verification_attempts = db.Column(db.Integer, default=0, nullable=False)
    last_verification_date = db.Column(db.DateTime)
    verification_comment = db.Column(db.String(t.LEN_INTERNAL_DB_COMMENT))

## Auth
# Define a User model
class User(UserMixin, Base):
    __tablename__ = 'auth_user'
    password    = db.Column(db.String(192), nullable=False)
    primary_email = db.Column(db.String(128), nullable=False, unique=True, \
            primary_key=True)
    email_verified = db.Column(db.Boolean, default=False, nullable=False)
    date_email_verified = db.Column(db.DateTime)
    display_name = db.Column(db.String(t.LEN_DISPLAY_NAME))
    description = db.Column(db.String(t.LEN_DESCRIPTION))
    display_image = db.Column(UploadedFileField( \
        upload_type=UploadedImageWithThumb, upload_storage='images'))
    educational_institution = db.Column(db.String(t.LEN_DISPLAY_NAME))
    can_create_departments = db.Column(db.Boolean, default=False, nullable=False)
    is_admin = db.Column(db.Boolean, default=False, nullable=False)

    email_addresses = db.relationship('Email', backref='user')
    matrix_addresses = db.relationship('Matrix', backref='user')
    developer = db.relationship('Developer', backref='user', uselist=False)

    def __repr__(self):
        return f'<User {self.name}>'

class Email(Base):
    __tablename__ = 'user_email_addresses'
    user_id = db.Column(db.String(t.LEN_UUID), db.ForeignKey('auth_user.id'),
            nullable=False)
    email = db.Column(db.String(128), nullable=False, unique=True, \
            primary_key=True)

    def __repr__(self):
        return f'<Email {self.email}>'

class Matrix(Base):
    __tablename__ = 'user_matrix_handles'
    user_id = db.Column(db.String(t.LEN_UUID), db.ForeignKey('auth_user.id'),
            nullable=False)
    handle = db.Column(db.String(128), nullable=False, unique=True, primary_key=True)

    def __repr__(self):
        return f'<Matrix {self.handle}>'

class CV(Base):
    __tablename__ = 'user_cvs'
    dev_id = db.Column(db.String(t.LEN_UUID), db.ForeignKey('developers.id'),
            nullable=False)
    document = db.Column('content_col', UploadedFileField)

class Developer(BaseRequiresVerification):
    __tablename__ = 'developers'
    user_id = db.Column(db.String(t.LEN_UUID), db.ForeignKey('auth_user.id'),
            nullable=False)
    cv = db.relationship('CV', backref='developer', uselist=False)

    projects = db.relationship('DeveloperProjectsMap',
        back_populates='developer')

    def __repr__(self):
        return f'<Developer {self.display_name}>'

user_organisations_map = db.Table('user_organisations_map',
    db.Column('user_id', db.String(t.LEN_UUID), db.ForeignKey('auth_user.id'), \
        primary_key=True),
    db.Column('organisation_id', db.String(t.LEN_UUID), db.ForeignKey('organisations.id'), \
        primary_key=True))

class Organisation(BaseRequiresVerification):
    __tablename__ = 'organisations'
    display_name = db.Column(db.String(t.LEN_DISPLAY_NAME), nullable=False)
    description = db.Column(db.String(t.LEN_DESCRIPTION), nullable=False)
    display_image = db.Column(UploadedFileField( \
        upload_type=UploadedImageWithThumb, upload_storage='images'))

    users = db.relationship('User', secondary=user_organisations_map,
        backref='organisations')
    departments = db.relationship('Department', backref='organisation')

    def __repr__(self):
        return f'<Organisation {self.display_name}>'

user_departments_map = db.Table('user_departments_map',
    db.Column('user_id', db.String(t.LEN_UUID), db.ForeignKey('auth_user.id'), \
        primary_key=True),
    db.Column('department_id', db.String(t.LEN_UUID), db.ForeignKey('departments.id'), \
        primary_key=True))

class DepartmentFile(Base):
    __tablename__ = 'department_files'
    document = db.Column('content_col', UploadedFileField)
    department_id = db.Column(db.String(t.LEN_UUID), \
        db.ForeignKey('departments.id'), nullable=False)

class Department(BaseRequiresVerification):
    __tablename__ = 'departments'
    display_name = db.Column(db.String(t.LEN_DISPLAY_NAME), nullable=False)
    description = db.Column(db.String(t.LEN_DESCRIPTION), nullable=False)
    display_image = db.Column(UploadedFileField( \
        upload_type=UploadedImageWithThumb, upload_storage='images'))
    organisation_id = db.Column(db.String(t.LEN_UUID), \
        db.ForeignKey('organisations.id'))
    temp_organisation = db.Column(db.String(t.LEN_DISPLAY_NAME))
    supporting_evidence = db.relationship('DepartmentFile', backref='department')

    users = db.relationship('User', secondary=user_departments_map,
        backref='departments')

    def __repr__(self):
        return f'<Department {self.display_name}>'

class DeveloperProjectsMap(Base):
    __tablename__ = 'developer_projects_map'
    developer_id = db.Column(db.String(t.LEN_UUID), db.ForeignKey('developers.id'),
        primary_key=True)
    project_id = db.Column(db.String(t.LEN_UUID), db.ForeignKey('projects.id'),
        primary_key=True)
    role = db.Column(db.Enum(t.DeveloperProjectStatus), nullable=False,
        default=t.DeveloperProjectStatus.not_related)

    developer = db.relationship('Developer', back_populates='projects')
    project = db.relationship('Project', back_populates='developers')

## Projects
project_tags_map = db.Table('project_tags_map',
    db.Column('project_id', db.String(t.LEN_UUID), db.ForeignKey('projects.id'),
        primary_key=True),
    db.Column('project_tag_id', db.String(t.LEN_UUID), db.ForeignKey('project_tags.id'),
        primary_key=True)
)

# Define a project model
class Project(Base):
    __tablename__ = 'projects'

    display_name = db.Column('title', db.String(t.LEN_DISPLAY_NAME), nullable=False)
    description = db.Column(db.String(t.LEN_DESCRIPTION), nullable=False)
    ect = db.Column(db.Integer)
    price = db.Column(db.Numeric(t.LEN_PRICE, 2))
    display_image = db.Column(db.String(t.LEN_URL))
    tags = db.relationship('ProjectTag', secondary=project_tags_map,
        backref='projects')

    developers = db.relationship('DeveloperProjectsMap',
        back_populates='project')
    department_id = db.Column(db.String(t.LEN_UUID), \
            db.ForeignKey('departments.id'), nullable=False)
    department = db.relationship('Department', backref='projects')

# Should always override id on initialisation to something human-readable
# https://sqlalchemy-utils.readthedocs.io/en/latest/data_types.html#module-sqlalchemy_utils.types.color
class ProjectTag(Base):
    __tablename__ = 'project_tags'
    display_name = db.Column(db.String(t.LEN_TAG))
    colour = db.Column(ColorType)

    def __repr__(self):
        return f'<ProjectTag {self.id}>'

# Blog-related things
class BlogPost(Base):
    __tablename__ = 'blog_posts'

    title = db.Column(Text(), nullable=False)
    url_id = db.Column(Text(), nullable=False)
    display_image = db.Column(UploadedFileField( \
        upload_type=UploadedImageWithThumb, upload_storage='blog_images'))
    author = db.Column(Text(), nullable=False)
    description = db.Column(Text(), nullable=False)
    body_html = db.Column(Text(), nullable=False)
    # Whether to render the post on the portfolio page
    is_portfolio = db.Column(db.Boolean, default=False, nullable=False)
