from app import db

# Define constants
LEN_USER_NAME = 30
LEN_DISPLAY_NAME = 60
LEN_DESCRIPTION = 500

# Define a base model for other database tables to inherit
class Base(db.Model):
    __abstract__  = True
    id            = db.Column(db.Integer, primary_key=True)
    date_created  = db.Column(db.DateTime,  default=db.func.current_timestamp())
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
    organisations = db.relationship('Organisation', backref='user')

    def __repr__(self):
        return f'<User {self.name}>'

class Email(Base):
    __tablename__ = 'user_email_addresses'
    email = db.Column(db.String(128), nullable=False, unique=True)

    def __repr__(self):
        return f'<Email {self.email}>'

class Matrix(Base):
    __tablename__ = 'user_matrix_handles'
    handle = db.Column(db.String(128), nullable=False, unique=True)

    def __repr__(self):
        return f'<Matrix {self.handle}>'

class Developer(Base):
    __tablename__ = 'developers'
    display_name = db.Column(db.String(LEN_DISPLAY_NAME))
    description = db.Column(db.String(LEN_DESCRIPTION))

    def __repr__(self):
        return f'<Developer {self.display_name}>'

class Organisation(Base):
    __tablename__ = 'organisations'
    display_name = db.Column(db.String(LEN_DISPLAY_NAME))
    description = db.Column(db.String(LEN_DESCRIPTION))
    #projects = db.relationship('Project', backref='organisation')

    def __repr__(self):
        return f'<Organisation {self.display_name}>'

developer_projects_map = db.Table('tags', 
    db.Column('developer_id', db.Integer, db.ForeignKey('developers.id'), 
        primary_key=True),
    db.Column('project_id', db.Integer, db.ForeignKey('projects.id'),
        primary_key=True),
    db.Column('role', db.String(60), nullable=False)
)

class Project(Base):
    ___tablename__ = 'projects'
    developers = db.relationship('Developer', secondary=developer_projects_map, 
        backref=db.backref('pages'))
    organisation = db.relationship('Organisation', backref='project')

    def __repr__(self):
        return f'<Project {self.id}>'
