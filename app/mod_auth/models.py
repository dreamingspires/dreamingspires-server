from app import db
from depot.fields.sqlalchemy import UploadedFileField
import uuid

# Define constants
LEN_USER_NAME = 30
LEN_DISPLAY_NAME = 60
LEN_DESCRIPTION = 500
LEN_UUID=32

# Define a base model for other database tables to inherit
class Base(db.Model):
    __abstract__  = True
    id = db.Column(db.String(LEN_UUID), primary_key=True, default=uuid.uuid4().hex)
    date_created = db.Column(db.DateTime,  default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime,  default=db.func.current_timestamp(),
                                           onupdate=db.func.current_timestamp())

# Define a User model
class User(Base):
    __tablename__ = 'auth_user'
    user_name = db.Column(db.String(LEN_USER_NAME), nullable=False, \
            primary_key=True, unique=True)
    password    = db.Column(db.String(192), nullable=False)
    email_addresses = db.relationship('Email', backref='user')
    matrix_addresses = db.relationship('Matrix', backref='user')
    developer = db.relationship('Developer', backref='user', uselist=False)
#    organisation_ids = db.Column(db.Integer, db.ForeignKey('organisations.id'),
#            nullable=False)
#    organisations = db.relationship('Organisation', backref='user')

    def __repr__(self):
        return f'<User {self.name}>'

class Email(Base):
    __tablename__ = 'user_email_addresses'
    user_ids = db.Column(db.String(LEN_UUID), db.ForeignKey('auth_user.id'),
            nullable=False)
    email = db.Column(db.String(128), nullable=False, unique=True, \
            primary_key=True)

    def __repr__(self):
        return f'<Email {self.email}>'

class Matrix(Base):
    __tablename__ = 'user_matrix_handles'
    user_ids = db.Column(db.String(LEN_UUID), db.ForeignKey('auth_user.id'),
            nullable=False)
    handle = db.Column(db.String(128), nullable=False, unique=True, primary_key=True)

    def __repr__(self):
        return f'<Matrix {self.handle}>'

class CV(Base):
    __tablename__ = 'user_cvs'
    document = db.Column('content_col', UploadedFileField)

class Developer(Base):
    __tablename__ = 'developers'
    user_ids = db.Column(db.String(LEN_UUID), db.ForeignKey('auth_user.id'),
            nullable=False)
    display_name = db.Column(db.String(LEN_DISPLAY_NAME))
    description = db.Column(db.String(LEN_DESCRIPTION))
    cv_id = db.Column(db.String(LEN_UUID), db.ForeignKey('user_cvs.id'), \
            nullable=False)
    cv = db.relationship('CV', backref='developer')

    def __repr__(self):
        return f'<Developer {self.display_name}>'

user_organisations_map = db.Table('association',
    db.Column('user_id', db.String(LEN_UUID), db.ForeignKey('auth_user.id'), \
        primary_key=True),
    db.Column('organisation_id', db.String(LEN_UUID), db.ForeignKey('organisations.id'), \
        primary_key=True))

#class UserOrganisationsMap(Base):
#    __tablename__ = 'user_organisations_map'
#    user_id = db.Column(db.Integer, db.ForeignKey('auth_user.id'), \
#        primary_key=True)
#    organisation_id = db.Column(db.Integer, db.ForeignKey('auth_user.id'), \
#        primary_key=True)

class Organisation(Base):
    __tablename__ = 'organisations'
    display_name = db.Column(db.String(LEN_DISPLAY_NAME))
    description = db.Column(db.String(LEN_DESCRIPTION))
    users = db.relationship('User', secondary=user_organisations_map,
        backref=db.backref('organisations'))
    #projects = db.relationship('Project', backref='organisation')

    def __repr__(self):
        return f'<Organisation {self.display_name}>'

developer_projects_map = db.Table('tags', 
    db.Column('developer_id', db.String(LEN_UUID), db.ForeignKey('developers.id'), 
        primary_key=True),
    db.Column('project_id', db.String(LEN_UUID), db.ForeignKey('projects.id'),
        primary_key=True),
    db.Column('role', db.String(60))
)

class Project(Base):
    __tablename__ = 'projects'
    developers = db.relationship('Developer', secondary=developer_projects_map, 
        backref=db.backref('projects'))
    organisation_id = db.Column(db.String(LEN_UUID), \
            db.ForeignKey('organisations.id'), nullable=False)
    organisation = db.relationship('Organisation', backref='projects')

    def __repr__(self):
        return f'<Project {self.id}>'
