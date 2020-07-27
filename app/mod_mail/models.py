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
from sqlalchemy.sql.expression import asc

# Define constants
LEN_USER_NAME = 30
LEN_DISPLAY_NAME = 60
LEN_DESCRIPTION = 500
LEN_UUID=32
LEN_PRICE=10
LEN_URL=60
LEN_TAG = 20

LEN_GROUP_NAME = 100
LEN_MAIL = 10000

from app.models import Base, User

## Mail
# Messages in the group are ordered by date_created
group_user_map = db.Table('group_user_map',
    db.Column('group_id', db.String(LEN_UUID),
        db.ForeignKey('mail_groups.id'), primary_key=True),
    db.Column('user_id', db.String(LEN_UUID),
        db.ForeignKey('auth_user.id'), primary_key=True),
#    info={'bind_key': 'mail_db'}
)

group_message_map = db.Table('group_message_map',
    db.Column('group_id', db.String(LEN_UUID),
        db.ForeignKey('mail_groups.id'), primary_key=True),
    db.Column('message_id', db.String(LEN_UUID),
        db.ForeignKey('mail_messages.id'), primary_key=True),
#    info={'bind_key': 'mail_db'}
)

class MailGroup(Base):
    __tablename__ = 'mail_groups'
#    __bind_key__ = 'mail_db'
    display_name = db.Column('group_display_name', db.String(LEN_GROUP_NAME), nullable=False)
    display_image = db.Column(db.String(LEN_URL))
    users = db.relationship('User', secondary=group_user_map,
        backref='mail')
    messages = db.relationship('MailMessage', secondary=group_message_map,
        backref='mail', order_by="asc(MailMessage.date_created)")
    read_receipts = db.relationship('ReadReceipt', backref='group')

class MailMessage(Base):
    __tablename__ = 'mail_messages'
#    __bind_key__ = 'mail_db'
    user_id = db.Column('user_id', db.String(LEN_UUID),
        db.ForeignKey('auth_user.id'), primary_key=True)
    user = db.relationship('User')
    body = db.Column(db.String(LEN_MAIL), nullable=False)

# The timestamp of the ReadReceipt is date_modified
class ReadReceipt(Base):
    __tablename__ = 'mail_read_receipts'
#    __bind_key__ = 'mail_db'
    user_id = db.Column('user_id', db.String(LEN_UUID),
        db.ForeignKey('auth_user.id'), primary_key=True)
    user = db.relationship('User')
    group_id = db.Column('group_id', db.String(LEN_UUID),
        db.ForeignKey('mail_groups.id'), primary_key=True)
