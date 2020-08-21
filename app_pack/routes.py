from flask import Flask, render_template, session, redirect, url_for, session, flash, request
from flask_wtf import FlaskForm
from wtforms import (StringField, BooleanField, DateTimeField,
                     RadioField,SelectField,TextField,
                     TextAreaField,SubmitField)

from wtforms.validators import DataRequired
from app_pack.forms import *

from app_pack import app, db
from app_pack.models import Rucher, Ruche, User
from flickr_api import Photo, Walker

import requests, random
from werkzeug.exceptions import NotFound  
from flask_login import login_user, login_required, logout_user

import json
from geojson import Point, Feature                   


def create_position(id, title, latitude, longitude, description):
    point = Point([longitude, latitude])
    properties = {
        "title": title,
        "description": description,
        'icon': "campsite",
        'marker-color': '#3bb2d0',
        'marker-symbol': id,
    }
    feature = Feature(geometry = point, properties = properties)
    return feature


def create_positions_details():

    positions = []

    #print(Rucher.query.with_entities(Rucher.lat, Rucher.longit).all())

    for rucher in Rucher.query.all():

        position = create_position(
            rucher.id,
            rucher.location,
            rucher.lat,
            rucher.longit,
            str(rucher)
        )
        positions.append(position)

    return positions


@app.route('/')
def index():
    print(User.__table__.c)
    return render_template('home.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You logged out!')
    return redirect(url_for('index'))

@app.route('/login', methods=['GET', 'POST'])
def login():

    form = LoginForm()
    if form.validate_on_submit():
        # Grab the user from our User Models table
        user = User.query.filter_by(email=form.email.data).first()
        
        # Check that the user was supplied and the password is right
        # The verify_password method comes from the User object
        # https://stackoverflow.com/questions/2209755/python-operation-vs-is-not

        if user.check_password(form.password.data) and user is not None:
            #Log in the user

            login_user(user)
            flash('Connexion réussie!')

            # If a user was trying to visit a page that requires a login
            # flask saves that URL as 'next'.
            next = request.args.get('next')

            # So let's now check if that next exists, otherwise we'll go to
            # the welcome page.
            if next == None or not next[0]=='/':
                next = url_for('see_ruchers')

            return redirect(next)
    return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        user = User(email=form.email.data,
                    username=form.name.data,
                    password=form.password.data)

        db.session.add(user)
        db.session.commit()
        flash('Merci de vous etre enregistré(e). Vous pouvez maintenant vous connecter')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)


@app.route('/see_ruchers')
@login_required
def see_ruchers():

    positions = create_positions_details()

    ruchers = Rucher.query.all()

    return render_template('ruchers.html', ruchers=ruchers, positions = positions)

@app.route('/add_rucher', methods=['GET', 'POST'])
@login_required
def add_rucher():

    positions = create_positions_details()
    form = RucherAddForm()

    if form.validate_on_submit():   

        if Rucher.query.filter(Rucher.location == form.location.data):
            flash("Un rucher exister déja a {}. Renseigner une localisation différente".format(form.location.data))
            return redirect('#')
            
        new_rucher = Rucher(location=form.location.data, plants=form.plant.data, feedback=form.feedback.data, lat=form.lat.data, longit=form.longit.data)
        db.session.add(new_rucher) # new_rucher.id added here
        db.session.commit()

        return redirect('/')

    return render_template('add_rucher.html', form=form, positions=positions)

@app.route('/delete_rucher/<id>', methods=['POST'])      
@login_required
def delete_rucher(id):
    #Ruche.query.filter_by(rucher=id).delete()
    db.session.delete(Rucher.query.get(id))
    db.session.commit()
    return redirect('/')


@app.route('/delete_ruche/<id>', methods=['POST'])
@login_required
def delete_ruche(id):
    id_rucher = Ruche.query.get(id).rucher
    db.session.delete(Ruche.query.get(id))
    db.session.commit()
    return redirect(url_for('see_rucher', id=id_rucher))

@app.route('/update_ruche/<id>', methods=['GET', 'POST'])
@login_required
def update_ruche(id):

    old_ruche = Ruche.query.get(id)
    list_species = [(i.specie, i.specie) for i in db.session.query(Ruche).all()]
    # list_species2 = [(g.specie, g.specie) for g in Ruche.query.all()]
    list_species.append(('other', 'autre'))
    list_species = list(set(list_species))

    form = RucheForm()
    form.breed.choices = list_species
    form.num.data = old_ruche.num

    if form.validate_on_submit():

        print("update ruche form")
        id_rucher = Ruche.query.get(id).rucher
        print(id_rucher)
        specie = form.breed.data
        print(specie, form.new_breed.data)
        if specie == "other":
            specie = form.new_breed.data

        old_ruche.specie = specie
        old_ruche.age_reine = form.age_queen.data
        old_ruche.feedback = form.feedback.data
        old_ruche.rucher = form.rucher.data
        db.session.commit()

        return redirect(url_for('see_rucher', id=id_rucher))    

    return render_template('update_ruche.html', ruche=old_ruche, form=form)


@app.route('/rucher/<id>', methods=['GET', 'POST'])
@login_required
def see_rucher(id):

    rucher = Rucher.query.get(id)

    if not rucher:
        raise NotFound    

    list_species = [(i.specie, i.specie) for i in db.session.query(Ruche).all()]
    # list_species2 = [(g.specie, g.specie) for g in Ruche.query.all()]
    list_species.append(('other', 'autre'))
    list_species = list(set(list_species))
    form = RucheForm()
    form.breed.choices = list_species

    if form.validate_on_submit():

        specie = form.new_breed.data

        if not specie:
            specie = form.breed.data

        # check ruche num is unique
        if Ruche.query.filter(Ruche.num == form.num.data).first():
            
            flash("La ruche {} existe déja".format(form.num.data))
            return redirect('#')
        
        new_ruche = Ruche(rucher=id, specie=specie, num=form.num.data, age_reine=form.age_queen.data,  feedback=form.feedback.data)
        db.session.add(new_ruche)
        db.session.commit()
        
        return redirect('#')    

    return render_template('rucher.html', ruches=rucher.get_ruches(), rucher=rucher, form=form)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(reload= True, debug=True)
