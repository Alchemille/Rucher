from app_pack import db, login_manager # created in init file
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
    longitude = db.Column(db.Float)
    latitude = db.Column(db.Float)

    def __init__(self, *args, **kwargs): # note: in other models, no init method -> use the one of db.Model, which accepts any argument.
        # in Python, a class has only 1 constructor !
        kwargs['password_hash'] = generate_password_hash(kwargs.pop('password'))
        super().__init__(*args, **kwargs)
  

    def check_password(self,password):
        # https://stackoverflow.com/questions/23432478/flask-generate-password-hash-not-constant-output
        return check_password_hash(self.password_hash,password)

class Rucher(db.Model):

    user = db.Column(db.Integer, db.ForeignKey('users.id'))
    id = db.Column(db.Integer, primary_key=True)
    location = db.Column(db.String(64), index=True)
    plants = db.Column(db.String(120))
    frelons_asiat = db.Column(db.Integer)
    lat = db.Column(db.Float)
    longit = db.Column(db.Float)
    ruches = db.relationship('Ruche', backref='parent', cascade = "all,delete",  lazy='dynamic')
    events = db.relationship('Event', backref='rucher_events', cascade='all,delete', order_by="Event.timestamp", lazy='dynamic')
    specie = db.Column(db.String(64), index=True)

    def get_ruches(self):

        ruches = Ruche.query.filter_by(rucher=self.id).all()
        return ruches


class Ruche(db.Model):
    
    rucher = db.Column(db.Integer, db.ForeignKey('rucher.id'))
    user = db.Column(db.Integer, db.ForeignKey('users.id'))
    id = db.Column(db.Integer, primary_key=True)
    num = db.Column(db.Integer)
    feedback = db.Column(db.Text)
    age_reine = db.Column(db.Integer, index=True)
    origin = db.Column(db.String(64))
    events = db.relationship('Event', backref='parent_ruche', cascade='all,delete', order_by="Event.timestamp", lazy='dynamic')

    __table_args__ = (db.UniqueConstraint('num', 'user', name='numruche_user_unique'),)    

class Event(db.Model):

    rucher = db.Column(db.Integer, db.ForeignKey('rucher.id'))
    ruche = db.Column(db.Integer, db.ForeignKey('ruche.id'))
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime)
    type = db.Column(db.String(64), index=True)
    note = db.Column(db.String(64))
    harvests = db.relationship('Harvest', backref='parent_event', cascade='all,delete', lazy='dynamic')

class Harvest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    event = db.Column(db.Integer, db.ForeignKey('event.id'))
    weight = db.Column(db.Integer)
    supers = db.Column(db.Integer)