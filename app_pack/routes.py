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
from flask_login import login_user, login_required, logout_user, current_user

import json
from geojson import Point, Feature       

import flask_login


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


def create_positions_details(ruchers):

    positions = []

    #print(Rucher.query.with_entities(Rucher.lat, Rucher.longit).all())

    for rucher in ruchers:

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
    print(Rucher.__table__.c)
    print(Ruche.__table__.c)
    return render_template('home.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You logged out!')
    return redirect(url_for('index'))

@app.route('/login', methods=['GET', 'POST'])
def login():

    if current_user.is_authenticated:
        return redirect(url_for('index'))    

    form = LoginForm()
    if form.validate_on_submit():
        # Grab the user from our User Models table
        user = User.query.filter_by(email=form.email.data).first()
        
        # Check that the user was supplied and the password is right
        # The verify_password method comes from the User object
        # https://stackoverflow.com/questions/2209755/python-operation-vs-is-not

        if user.check_password(form.password.data) and user is not None:

            login_user(user, remember=form.remember_me.data)
            flash('Connexion réussie!')
            next = request.args.get('next')
            if next == None or not next[0]=='/':
                next = url_for('see_ruchers')

            return redirect(next)

        else:
            flash("Email ou mot de passe invalide")

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

    ruchers = Rucher.query.filter_by(user=current_user.id).all()

    positions = create_positions_details(ruchers)

    return render_template('ruchers.html', ruchers=ruchers, positions = positions)



@app.route('/rucher/<id>', methods=['GET', 'POST'])
@login_required
def see_rucher(id):

    if not Rucher.query.get(id) or current_user.id != Rucher.query.get(id).user:
        flash("Vous n'avez pas l'autorisation d'effectuer cette opération")    
        return redirect(url_for('see_ruchers'))   

    form = RucheForm(rucher=id)
    form.specie_select.choices = get_species()
    form.rucher.choices = get_names_ruchers()
    print(get_names_ruchers())
    rucher = Rucher.query.get(id)

    if form.validate_on_submit():

        specie = form.specie.data
        if not specie:
            specie = form.specie_select.data

        new_ruche = Ruche(user=current_user.id, rucher=form.rucher.data, specie=specie, num=form.num.data, age_reine=form.age_reine.data,  feedback=form.feedback.data)
        db.session.add(new_ruche)
        db.session.commit()
        
        return redirect('#')    

    return render_template('rucher.html', ruches=rucher.get_ruches(), rucher=rucher, form=form)


@app.route('/add_rucher', methods=['GET', 'POST'])
@login_required
def add_rucher():

    ruchers = Rucher.query.filter_by(user=current_user.id).all()
    positions = create_positions_details(ruchers)
    form = RucherAddForm()

    if form.validate_on_submit():   
 
        new_rucher = Rucher(user=current_user.id, location=form.location.data, plants=form.plants.data, feedback=form.feedback.data, lat=form.lat.data, longit=form.longit.data)
        db.session.add(new_rucher) # new_rucher.id added here
        db.session.commit()

        return redirect(url_for('see_ruchers'))

    return render_template('add_rucher.html', form=form, positions=positions)

@app.route('/update_rucher/<id>', methods=['GET','POST'])      
@login_required
def update_rucher(id):

    if not Rucher.query.get(id) or current_user.id != Rucher.query.get(id).user:
        flash("Vous n'avez pas l'autorisation d'effectuer cette opération")
        return redirect(url_for('see_ruchers'))

    old_rucher = Rucher.query.get(id)
    form = RucherAddForm(obj=old_rucher)

    if form.validate_on_submit():

        form.populate_obj(old_rucher)

        db.session.commit()

        flash("Rucher modifié avec succes")

        return redirect(url_for('see_rucher', id=id))    

    return render_template('update_rucher.html', rucher=old_rucher, form=form)



@app.route('/delete_rucher/<id>', methods=['POST'])      
@login_required
def delete_rucher(id):

    if not Rucher.query.get(id) or current_user.id != Rucher.query.get(id).user:
        flash("Vous n'avez pas l'autorisation d'effectuer cette opération")
    else:
        #Ruche.query.filter_by(rucher=id).delete()
        db.session.delete(Rucher.query.get(id))
        db.session.commit()
        
    return redirect(url_for('see_ruchers'))

def get_species():

    ruches = Ruche.query.filter_by(user=current_user.id).all()
    list_species = [(i.specie, i.specie) for i in ruches]
    list_species.append(('other', 'autre'))
    list_species = list(set(list_species))
    return list_species

def get_names_ruchers():
    
    ruchers = Rucher.query.filter_by(user=current_user.id).all()
    list_ruchers = [(i.id, i.location) for i in ruchers]
    return list_ruchers

@app.route('/update_ruche/<id>', methods=['GET', 'POST'])
@login_required
def update_ruche(id):

    if not Ruche.query.get(id) or current_user.id != Ruche.query.get(id).user:
        flash("Vous n'avez pas l'autorisation d'effectuer cette opération")    
        return redirect(url_for('see_ruchers'))

    old_ruche = Ruche.query.get(id)
    form = RucheForm(obj=old_ruche)
    form.specie_select.choices = get_species()
    form.rucher.choices = get_names_ruchers()

    if form.validate_on_submit():

        form.populate_obj(old_ruche)

        specie = form.specie.data
        if not specie:
            specie = form.specie_select.data

        old_ruche.specie = specie
        db.session.commit()

        flash("Ruche modifiée avec succes")
        return redirect(url_for('see_rucher', id=form.rucher.data))    

    return render_template('update_ruche.html', ruche=old_ruche, form=form)



@app.route('/delete_ruche/<id>', methods=['POST'])
@login_required
def delete_ruche(id):

    if not Ruche.query.get(id) or current_user.id != Ruche.query.get(id).user:
        flash("Vous n'avez pas l'autorisation d'effectuer cette opération")    
        return redirect(url_for('see_ruchers'))

    id_rucher = Ruche.query.get(id).rucher
    db.session.delete(Ruche.query.get(id))
    db.session.commit()
    return redirect(url_for('see_rucher', id=id_rucher))


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
