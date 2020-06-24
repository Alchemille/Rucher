from flask import Flask, render_template, session, redirect, url_for, session, flash
from flask_wtf import FlaskForm
from wtforms import (StringField, BooleanField, DateTimeField,
                     RadioField,SelectField,TextField,
                     TextAreaField,SubmitField)

from wtforms.validators import DataRequired
from app_pack.forms import *

from app_pack import app, db
from app_pack.models import Rucher, Ruche
from flickr_api import Photo, Walker

import requests, random
from werkzeug.exceptions import NotFound  

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

    positions = create_positions_details()

    ruchers = Rucher.query.all()

    return render_template('ruchers.html', ruchers=ruchers, positions = positions)

@app.route('/add_rucher', methods=['GET', 'POST'])
def add_rucher():

    positions = create_positions_details()
    form = RucherAddForm()

    if form.validate_on_submit():

        new_rucher = Rucher(location=form.location.data, plants=form.plant.data, feedback=form.feedback.data, lat=form.lat.data, longit=form.longit.data)
        db.session.add(new_rucher)
        db.session.commit()

        #flash('Rucher {} ajouté'.format(form.location.data))

        return redirect('/')

    return render_template('add_rucher.html', form=form, positions=positions)

@app.route('/delete_rucher/<id>', methods=['POST'])      
def delete_rucher(id):
    #Ruche.query.filter_by(rucher=id).delete()
    db.session.delete(Rucher.query.get(id))
    db.session.commit()
    return redirect('/')

@app.route('/rucher/<id>', methods=['GET', 'POST'])
def see_rucher(id):

    rucher = Rucher.query.get(id)

    if not rucher:
        raise NotFound    

    list_species = [(i.specie, i.specie) for i in db.session.query(Ruche).all()]
    # print(list_species)
    # list_species2 = [(g.specie, g.specie) for g in Ruche.query.all()]
    # print(list_species2)
    list_species.append(('other', 'autre'))
    list_species = list(set(list_species))

    form = RucheForm()
    form.breed.choices = list_species

    if form.validate_on_submit():

        specie = form.breed.data
        print(specie, form.new_breed.data)
        if specie == "other":
            specie = form.new_breed.data

        new_ruche = Ruche(rucher=id, specie=specie, num=form.num.data, feedback=form.feedback.data)
        db.session.add(new_ruche)
        db.session.commit()

        return redirect('#')    

    return render_template('rucher.html', ruches=rucher.get_ruches(), form=form)

@app.route('/add_ruche/<rucher_id>')
def add_ruche(rucher_id):
    if form.validate_on_submit():

        new_ruche = Ruche(rucher=rucher_id, specie=form.breed.data, num=form.num.data, feedback=form.feedback.data)
        db.session.add(new_ruche)
        db.session.commit()

        return redirect('/rucher/<id>')

    return render_template('add_ruche.html', form=form)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(reload= True, debug=True)
