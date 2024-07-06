# from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from . import db

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True) #id for the db
    user_id = db.Column(db.String(50), unique=True, nullable=False) # actual user id for routing purposes
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    phone = db.Column(db.String(20), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow) # just to keep track of times users are created

    def __init__(self, user_id, first_name, last_name, email, password, phone=None):
        self.user_id = user_id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password_hash = generate_password_hash(password)
        self.phone = phone

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Organisation(db.Model):
    __tablename__ = 'organisations'
    
    id = db.Column(db.Integer, primary_key=True)
    org_id = db.Column(db.String(50), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, org_id, name, description=None):
        self.org_id = org_id
        self.name = name
        self.description = description

class UserOrganisation(db.Model): #an associate class just to make db interactions between users, orgs and userorgs easier :-)
    __tablename__ = 'user_organisations'
    
    user_id = db.Column(db.String(50), db.ForeignKey('users.user_id'), primary_key=True)
    org_id = db.Column(db.String(50), db.ForeignKey('organisations.org_id'), primary_key=True)
    joined_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', backref=db.backref('user_organisations', lazy=True))
    organisation = db.relationship('Organisation', backref=db.backref('user_organisations', lazy=True))

    def __init__(self, user_id, org_id):
        self.user_id = user_id
        self.org_id = org_id
