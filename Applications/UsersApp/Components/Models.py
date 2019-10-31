from sqlalchemy import create_engine, ForeignKey
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Date, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
# from flask import current_app
from flask_security import Security, SQLAlchemyUserDatastore, UserMixin, RoleMixin
# Intialize database:
engine = create_engine('sqlite:///webapp.db', echo=True)
Base = declarative_base()

db = SQLAlchemy()

# Models:
roles_users = db.Table('roles_users',
        db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
        db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))

class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

class User(db.Model, UserMixin):
    ''' User class for authentication purposes '''
    __tablename__ = "users"
    
    id = db.Column(db.Integer(), primary_key=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    name = db.Column(db.String(255))
    tel = db.Column(db.String(255))
    authenticated = db.Column(db.Boolean(), default=False)
    active = db.Column(db.Boolean(), default=True)
    confirmed_at = db.Column(db.DateTime())
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))

    def __init__(self, email, password, name, tel):

        self.email = email
        self.password = password
        self.name = name
        self.tel = tel

    def is_active(self):
        return self.active
        
    def get_id(self):
        return self.id
        
    def is_authenticated(self):
        return self.authenticated
    
    def is_anonymous(self):
        return False

from Applications.app import app

# Setup Flask-Security
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)

# Standalone execution:
if __name__ == '__main__':
    user_manager = UserManager(app, db, User)
    # Create tables:
    Base.metadata.create_all(engine)

