from flask import render_template,flash,redirect,url_for
from app import app, login
from app.forms import LoginForm, RegistrationForm, Kreiraj_izlet, Search, EditProfileForm
from flask_login import current_user, login_user,logout_user
from app.models import User
from app.models import Izlet
from flask_login import login_required
from flask import request
from werkzeug.urls import url_parse
from app import db
from sqlalchemy import text


@app.route('/')
@app.route('/index')
def index():
    izlet = Izlet.query.first_or_404()
    return render_template("obibsicima.html", title='Home Page', izlet=izlet)


@app.route('/prijava', methods=['GET', 'POST'])
def prijava():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('prijava'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('prijava.html', title='Prijava', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/registracija', methods=['GET', 'POST'])
def registracija():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, ime=form.ime.data, prezime=form.prezime.data, spol=form.spol.data, mjesto=form.mjesto.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('prijava'))
    return render_template('registracija.html', title='Registracija', form=form)


@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('user.html', user=user)



@app.route('/izlet/<id>')
@login_required
def izlet(id):
    izlett = Izlet.query.filter_by(id=id).first_or_404()
    sql = text('UPDATE izlet SET rezervirano = rezervirano+1 WHERE id = {};'.format(id))
    result = db.engine.execute(sql)
    return render_template("izlet.html", izlet=izlett)


@app.route('/kreiraj_izlet/', methods=['GET', 'POST'])
def kreiraj_izlet():
    form = Kreiraj_izlet()
    if form.validate_on_submit():
        izlet = Izlet(naziv=form.naziv.data, mjesto=form.mjesto.data, cijena=form.cijena.data, detalji=form.detalji.data, author=current_user, broj_putnika=form.broj_putnika.data, user_id=current_user.id, slika=form.slika.data)
        db.session.add(izlet)
        db.session.commit()
        flash('Dodali ste izlet!')
        return redirect(url_for('index'))
    return render_template('kreiraj_izlet.html', form=form)


@app.route('/izleti', methods=['GET', 'POST'])
@login_required
def izleti():
    izlet = Izlet.query.all()
    sql = text('UPDATE izlet SET rezervirano = rezervirano+1 WHERE id = 6;')
    result = db.engine.execute(sql)
    flash('Prijavili ste se na izlet!')
    return render_template("izleti.html", izlet=izlet)


@app.route('/pretraga', methods=['GET', 'POST'])
@login_required
def pretraga():
    form = Search()
    if form.validate_on_submit():
        search = form.search.data
        izlet = Izlet.query.filter(Izlet.mjesto.like("%" + search + "%")).all()
        return render_template("pretraga.html", form=form, izlet=izlet)
    izlet = Izlet.query.all()
    return render_template("pretraga.html", form=form, izlet=izlet)


@app.route('/single_izlet')
@login_required
def single_izlet():
    izlet = Izlet.query.first_or_404()
    return render_template("single_izlet.html", izlet=izlet)


@app.route('/single_profil/<username>')
@login_required
def single_profil(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('single_profil.html', user=user)


@app.route('/popis_izleta/')
@login_required
def popis_izleta():
    izlet = Izlet.query.filter_by(user_id=current_user.id).all()
    return render_template("popis_izleta.html", title='Home Page', izlet=izlet)


@app.route('/popis_izleta/delete', methods=['POST'])
@login_required
def delete(izlet_id):
    izlet = Izlet.query.filter_by(id=izlet_id)
    db.session.delete(izlet)
    db.session.commit()
    return redirect(url_for('popis_izleta'))


@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.ime = form.ime.data
        current_user.prezime = form.prezime.data
        current_user.spol = form.spol.data
        current_user.mjesto = form.mjesto.data
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.slika = form.slika.data
        db.session.commit()
        flash('Vase promjene su spremljene.')
        return redirect(url_for('user', username=current_user.username))
    elif request.method == 'GET':
        form.ime.data = current_user.ime
        form.prezime.data = current_user.prezime
        form.spol.data = current_user.spol
        form.mjesto.data = current_user.mjesto
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.slika.data = current_user.slika
    return render_template('edit_profile.html', title='Uredi Profil', form=form)


@app.route('/izlet_update/<id>', methods=['GET', 'POST'])
@login_required
def izlet_update(id):
    izlet = Izlet.query.get_or_404(id)
    if izlet.author != current_user:
        abort(403)
    form = Kreiraj_izlet()
    if form.validate_on_submit():
        izlet.naziv = form.naziv.data
        izlet.mjesto = form.mjesto.data
        izlet.cijena = form.cijena.data
        izlet.detalji = form.detalji.data
        izlet.broj_putnika = form.broj_putnika.data
        izlet.slika = form.slika.data
        db.session.commit()
        flash('Uredili ste izlet!')
        return redirect(url_for('izlet', id=izlet.id))
    elif request.method == 'GET':
        form.naziv.data = izlet.naziv
        form.mjesto.data = izlet.mjesto
        form.cijena.data = izlet.cijena
        form.detalji.data = izlet.detalji
        form.broj_putnika.data = izlet.broj_putnika
        form.slika.data = izlet.slika
    return render_template('uredi_izlet.html', form=form)


@app.route('/izlet/<id>/delete', methods=['POST'])
@login_required
def delete_izlet(id):
    izlet = Izlet.query.get_or_404(id)
    if izlet.author != current_user:
        abort(403)
    db.session.delete(izlet)
    db.session.commit()
    flash('Izbrisali ste izlet!')
    return redirect(url_for('index'))

