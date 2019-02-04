from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from app.models import User
from app.models import Izlet

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    ime = StringField('Ime', validators=[DataRequired()])
    prezime = StringField('Prezime', validators=[DataRequired()])
    spol = StringField('Spol', validators=[DataRequired()])
    mjesto = StringField('Mjesto', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')

class Kreiraj_izlet(FlaskForm):
    naziv = StringField('Naziv', validators=[DataRequired()])
    mjesto = StringField('Mjesto', validators=[DataRequired()])
    cijena = StringField('Cijena', validators=[DataRequired()])
    detalji = StringField('Detalji', validators=[DataRequired()])
    broj_putnika = StringField('Broj putnika', validators=[DataRequired()])
    slika = StringField('Url slike', validators=[DataRequired()])
    submit = SubmitField('Dodaj')

class Search(FlaskForm):
    search = StringField('Pretraga')
    submit = SubmitField('Pretraži')

class EditProfileForm(FlaskForm):
    ime = StringField('Ime')
    prezime = StringField('Prezime')
    spol = StringField('Spol')
    mjesto = StringField('Mjesto')
    username = StringField('Username')
    email = StringField('Email')
    slika = StringField('Url slike')
    submit = SubmitField('Edit')
