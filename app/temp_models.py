# Defines the database schemata used throughout the site
# Could maybe be separated into the separate blueprints, but all the
# tables are interdependent (such as Developers being linked to Users and
# Projects), so for now all the databases are defined here instead

from app import db
import app.types as t

from app.models import Base

class InterestedClient(Base):
    __tablename__ = 'interested_clients'
    __bind_key__ = 'temp_db'
    name = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(128), primary_key=True)
    phone = db.Column(db.String(128))
    organisation = db.Column(db.String(t.LEN_DISPLAY_NAME))
    estimated_cost = db.Column(db.String(20))
    project_description = db.Column(db.String(1000), nullable=False)
    actioned = db.Column(db.Boolean, server_default='0', nullable=False)
