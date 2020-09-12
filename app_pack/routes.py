from flask import Flask, render_template, session, redirect, url_for, session, flash, request, jsonify, make_response
from flask_wtf import FlaskForm
from wtforms import (StringField, BooleanField, DateTimeField,
                     RadioField,SelectField,TextField,
                     TextAreaField,SubmitField)

from wtforms.validators import DataRequired
from app_pack.forms import *

from app_pack import app, db
from app_pack.models import Rucher, Ruche, User, Event
from flickr_api import Photo, Walker

import requests, random
from werkzeug.exceptions import NotFound  
from flask_login import login_user, login_required, logout_user, current_user

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


def create_positions_details(ruchers):

    positions = []

    #print(Rucher.query.with_entities(Rucher.lat, Rucher.longit).all())

    for rucher in ruchers:

        position = create_position(
            rucher.id,
            rucher.location,
            rucher.lat,
            rucher.longit,
            str(len(rucher.get_ruches())) + " ruches" 
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

def get_name_rucher(rucher_id):
    rucher = Rucher.query.get(rucher_id).location
    return rucher


def get_types_events():

    q = db.session.query(
           Event,
        ).filter(
            Rucher.user == current_user.id,
        ).filter(
            Rucher.id == Event.rucher,
        ).all()
    list_types_events = [(i.type, i.type) for i in q]
    list_types_events.append(('other', 'autre'))
    list_types_events = list(set(list_types_events))
    return list_types_events

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

    error_to_ignore = ['La ruche {} existe déja'.format(old_ruche.num)]
    # ignore this error since the check_num_unique() validator should not be inforced if the num of the ruche is unchanged
    if form.validate_on_submit() or form.errors.get('num') == error_to_ignore:

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


@app.route('/events/', methods=['GET', 'POST'])
@login_required
def events():
    
    rucher = int(request.args.get("rucher", -1)) # if no rucher args, default is -1
    form = EventForm(request.form, rucher=rucher) # default rucher is either the one in args or let blank
    form.type_select.choices = get_types_events()

    if rucher != -1:    
        form.rucher.choices = [(rucher, get_name_rucher(rucher))]
    else:
        form.rucher.choices = get_names_ruchers()
        form.rucher.choices.append((-1, ''))

    if form.validate_on_submit():
        
        if not form.type.data:
            type = form.type_select.data
        else: type = form.type.data

        if form.ruche.data:
            id_parent_ruche = Ruche.query.filter_by(num=form.ruche.data, user=current_user.id).first().id
            new_event = Event(ruche=id_parent_ruche, rucher=Ruche.query.get(id_parent_ruche).rucher, timestamp=form.timestamp.data, type=type, note=form.note.data)

        else: 
            rucher_id = form.rucher.data
            new_event = Event(rucher=rucher_id, timestamp=form.timestamp.data, type=type, note=form.note.data)

        db.session.add(new_event)
        db.session.commit()

        return redirect('#')   

    type = request.args.get("type", "tous")
    form_search = SearchEvent(rucher=rucher, type_select=type)
    form_search.type_select.choices = get_types_events()
    form_search.type_select.choices.append(('tous', 'tous'))
    form_search.rucher.choices = get_names_ruchers()
    form_search.rucher.choices.append((-1, 'tous'))    

    events = Event.query.filter(Event.rucher_events.has(user=current_user.id))        
    return render_template('events.html', events=events, form=form, form_search=form_search)


@app.route('/search_events', methods=['GET'])
@login_required
def search_event():

    events = Event.query.filter(Event.rucher_events.has(user=current_user.id))
    req = request.args
    rucher = int(req["rucher"])
    type = req["type"]


    if rucher != -1:
        events = events.filter_by(rucher=rucher)
    if type != 'tous':
        events = events.filter_by(type=type)
    if req['ruche'] != "":
        ruche_of_interest = Ruche.query.filter_by(num=req['ruche']).first()
        rucher_of_interest = ruche_of_interest.rucher
        events = events.filter((Event.ruche==ruche_of_interest.id) | ((Event.rucher==rucher_of_interest) & (Event.ruche==None)))

    return render_template("event_table.html", events=events)


@app.route('/delete_event/<id>', methods=['POST'])
@login_required
def delete_event(id):

    if not Event.query.get(id) or current_user.id != Event.query.get(id).parent_ruche.user:
        flash("Vous n'avez pas l'autorisation d'effectuer cette opération")    
        return redirect(url_for('see_ruchers'))

    db.session.delete(Event.query.get(id))
    db.session.commit()
    return redirect(url_for('events'))

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
