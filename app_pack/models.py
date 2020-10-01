from app_pack import db, login_manager # created in init file
import requests
import random
import os.path
import urllib.request
from flask import url_for
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
# By inheriting the UserMixin we get access to a lot of built-in attributes
# which we will be able to call in our views!
# is_authenticated()
# is_active()
# is_anonymous()
# get_id()


# The user_loader decorator allows flask-login to load the current user
# and grab their id.
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class User(db.Model, UserMixin):
    
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    ruchers = db.relationship('Rucher', backref='owner', cascade="all,delete", lazy='dynamic')
    ruches = db.relationship('Ruche', backref='owner', cascade="all,delete", lazy='dynamic')
    registration_date = db.Column(db.DateTime, index=True)

    def __init__(self, email, username, password): # note: in other models, no init method -> use the one of db.Model, which accepts any argument.
        # in Python, a class has only 1 constructor !
        self.email = email
        self.username = username
        self.password_hash = generate_password_hash(password)

    def check_password(self,password):
        # https://stackoverflow.com/questions/23432478/flask-generate-password-hash-not-constant-output
        return check_password_hash(self.password_hash,password)

class Rucher(db.Model):

    user = db.Column(db.Integer, db.ForeignKey('users.id'))
    id = db.Column(db.Integer, primary_key=True)
    location = db.Column(db.String(64), index=True)
    plants = db.Column(db.String(120))
    feedback = db.Column(db.Text)
    lat = db.Column(db.Float)
    longit = db.Column(db.Float)
    ruches = db.relationship('Ruche', backref='parent', cascade = "all,delete",  lazy='dynamic')
    events = db.relationship('Event', backref='rucher_events', cascade='all,delete', lazy='dynamic')

    def get_ruches(self):

        ruches = Ruche.query.filter_by(rucher=self.id).all()
        return ruches


class Ruche(db.Model):
    
    rucher = db.Column(db.Integer, db.ForeignKey('rucher.id'))
    user = db.Column(db.Integer, db.ForeignKey('users.id'))
    id = db.Column(db.Integer, primary_key=True)
    num = db.Column(db.Integer)
    feedback = db.Column(db.Text)
    specie = db.Column(db.String(64), index=True)
    age_reine = db.Column(db.DateTime, index=True)
    events = db.relationship('Event', backref='parent_ruche', cascade='all,delete', lazy='dynamic')

    __table_args__ = (db.UniqueConstraint('num', 'user', name='numruche_user_unique'),)    

class Event(db.Model):

    rucher = db.Column(db.Integer, db.ForeignKey('rucher.id'))
    ruche = db.Column(db.Integer, db.ForeignKey('ruche.id'))
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime)
    type = db.Column(db.Integer, index=True)
    note = db.Column(db.String(64))