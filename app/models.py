from datetime import datetime
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login

class User(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ime = db.Column(db.String(64), index=True)
    prezime = db.Column(db.String(64), index=True)
    spol = db.Column(db.String(64), index=True)
    mjesto = db.Column(db.String(64), index=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    slika = db.Column(db.String(120), index=True, default="https://i.stack.imgur.com/34AD2.jpg")
    password_hash = db.Column(db.String(128))
    posts = db.relationship('Izlet', backref='author', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post {}>'.format(self.body)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class Izlet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    naziv = db.Column(db.String(140))
    mjesto = db.Column(db.String(140))
    cijena = db.Column(db.String(140))
    detalji = db.Column(db.Text)
    broj_putnika = db.Column(db.Integer)
    rezervirano = db.Column(db.Integer, default=0)
    slika = db.Column(db.String(140))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Izlet {}>'.format(self.detalji)

class Tablica(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    izlet_id = db.Column(db.Integer, db.ForeignKey('izlet.id'))
    rezervirano_mjesto = db.Column(db.Integer)
    prijava = db.Column(db.Integer)

    
    def __repr__(self):
        return '<Tablica {}>'.format(self.id)