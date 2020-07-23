# Defines the database schemata used throughout the site
# Could maybe be separated into the separate blueprints, but all the
# tables are interdependent (such as Developers being linked to Users and
# Projects), so for now all the databases are defined here instead

from app import db
from depot.fields.sqlalchemy import UploadedFileField
from flask_login import UserMixin
import uuid

from colour import Color
from sqlalchemy_utils import ColorType

# Define constants
LEN_USER_NAME = 30
LEN_DISPLAY_NAME = 60
LEN_DESCRIPTION = 500
LEN_UUID=32
LEN_PRICE=10
LEN_URL=60
LEN_TAG = 20

# Define a base model for other database tables to inherit
class Base(db.Model):
    __abstract__  = True
    id = db.Column(db.String(LEN_UUID), primary_key=True, default=uuid.uuid4().hex)
    date_created = db.Column(db.DateTime,  default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime,  default=db.func.current_timestamp(),
                                           onupdate=db.func.current_timestamp())

## Auth
# Define a User model
class User(UserMixin, Base):
    __tablename__ = 'auth_user'
    user_name = db.Column(db.String(LEN_USER_NAME), nullable=False, \
            primary_key=True, unique=True)
    password    = db.Column(db.String(192), nullable=False)
    primary_email = db.Column(db.String(128), nullable=False, unique=True, \
            primary_key=True)
    display_name = db.Column(db.String(LEN_DISPLAY_NAME))
    description = db.Column(db.String(LEN_DESCRIPTION))

    email_addresses = db.relationship('Email', backref='user')
    matrix_addresses = db.relationship('Matrix', backref='user')
    developer = db.relationship('Developer', backref='user', uselist=False)
#    department_ids = db.Column(db.Integer, db.ForeignKey('departments.id'),
#            nullable=False)
#    departments = db.relationship('Department', backref='user')

    def __repr__(self):
        return f'<User {self.name}>'

class Email(Base):
    __tablename__ = 'user_email_addresses'
    user_id = db.Column(db.String(LEN_UUID), db.ForeignKey('auth_user.id'),
            nullable=False)
    email = db.Column(db.String(128), nullable=False, unique=True, \
            primary_key=True)

    def __repr__(self):
        return f'<Email {self.email}>'

class Matrix(Base):
    __tablename__ = 'user_matrix_handles'
    user_id = db.Column(db.String(LEN_UUID), db.ForeignKey('auth_user.id'),
            nullable=False)
    handle = db.Column(db.String(128), nullable=False, unique=True, primary_key=True)

    def __repr__(self):
        return f'<Matrix {self.handle}>'

class CV(Base):
    __tablename__ = 'user_cvs'
    dev_id = db.Column(db.String(LEN_UUID), db.ForeignKey('developers.id'),
            nullable=False)
    document = db.Column('content_col', UploadedFileField)
    

class Developer(Base):
    __tablename__ = 'developers'
    user_id = db.Column(db.String(LEN_UUID), db.ForeignKey('auth_user.id'),
            nullable=False)
    cv = db.relationship('CV', backref='developer')

    def __repr__(self):
        return f'<Developer {self.display_name}>'

user_organisations_map = db.Table('user_organisations_map',
    db.Column('user_id', db.String(LEN_UUID), db.ForeignKey('auth_user.id'), \
        primary_key=True),
    db.Column('organisation_id', db.String(LEN_UUID), db.ForeignKey('organisations.id'), \
        primary_key=True))

class Organisation(Base):
    __tablename__ = 'organisations'
    display_name = db.Column(db.String(LEN_DISPLAY_NAME), nullable=False)
    description = db.Column(db.String(LEN_DESCRIPTION), nullable=False)
    users = db.relationship('User', secondary=user_organisations_map,
        backref='organisations')
    departments = db.relationship('Department', backref='organisation')

    def __repr__(self):
        return f'<Organisation {self.display_name}>'

user_departments_map = db.Table('user_departments_map',
    db.Column('user_id', db.String(LEN_UUID), db.ForeignKey('auth_user.id'), \
        primary_key=True),
    db.Column('department_id', db.String(LEN_UUID), db.ForeignKey('departments.id'), \
        primary_key=True))

class Department(Base):
    __tablename__ = 'departments'
    display_name = db.Column(db.String(LEN_DISPLAY_NAME))
    description = db.Column(db.String(LEN_DESCRIPTION))
    users = db.relationship('User', secondary=user_departments_map,
        backref='departments')
    organisation_id = db.Column(db.String(LEN_UUID), db.ForeignKey('organisations.id'))
    #projects = db.relationship('Project', backref='department')

    def __repr__(self):
        return f'<Department {self.display_name}>'

developer_projects_map = db.Table('developer_projects_map', 
    db.Column('developer_id', db.String(LEN_UUID), db.ForeignKey('developers.id'), 
        primary_key=True),
    db.Column('project_id', db.String(LEN_UUID), db.ForeignKey('projects.id'),
        primary_key=True),
    db.Column('role', db.String(60))
)

## Projects
project_tags_map = db.Table('project_tags_map',
    db.Column('project_id', db.String(LEN_UUID), db.ForeignKey('projects.id'),
        primary_key=True),
    db.Column('project_tag_id', db.String(LEN_UUID), db.ForeignKey('project_tags.id'),
        primary_key=True)
)

# Define a project model
class Project(Base):
    __tablename__ = 'projects'

    display_name = db.Column('title', db.String(LEN_DISPLAY_NAME), nullable=False)
    description = db.Column(db.String(LEN_DESCRIPTION), nullable=False)
    ect = db.Column(db.Integer)
    price = db.Column(db.Numeric(LEN_PRICE, 2))
    display_image = db.String(LEN_URL)
    tags = db.relationship('ProjectTag', secondary=project_tags_map,
        backref='projects')

    developers = db.relationship('Developer', secondary=developer_projects_map, 
        backref='projects')
    department_id = db.Column(db.String(LEN_UUID), \
            db.ForeignKey('departments.id'), nullable=False)
    department = db.relationship('Department', backref='projects')

# Should always override id on initialisation to something human-readable
# https://sqlalchemy-utils.readthedocs.io/en/latest/data_types.html#module-sqlalchemy_utils.types.color
class ProjectTag(Base):
    __tablename__ = 'project_tags'
    display_name = db.Column(db.String(LEN_TAG))
    colour = db.Column(ColorType)

    def __repr__(self):
        return f'<ProjectTag {self.id}>'
