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
    point = Point([latitude, longitude])
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

    print(Rucher.query.with_entities(Rucher.lat, Rucher.longit).all())

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
    print(positions)

    ruchers = Rucher.query.all()

    return render_template('ruchers.html', ruchers=ruchers, positions = positions)

@app.route('/add_rucher', methods=['GET', 'POST'])
def add_rucher():

    form = RucherAddForm()
    if form.validate_on_submit():

        new_rucher = Rucher(location=form.location.data, plants=form.plant.data, feedback=form.feedback.data, lat=form.lat.data, longit=form.longit.data)
        db.session.add(new_rucher)
        db.session.commit()

        #flash('Rucher {} ajouté'.format(form.location.data))

        return redirect('/')

    return render_template('add_rucher.html', form=form)

@app.route('/delete_rucher/<id>', methods=['POST'])      
def delete_rucher(id):
    db.session.delete(Rucher.query.get(id))
    db.session.commit()
    return redirect('/')

@app.route('/rucher/<id>', methods=['GET', 'POST'])
def see_rucher(id):

    rucher = Rucher.query.get(id)

    if not rucher:
        raise NotFound    

    form = RucheForm()
    if form.validate_on_submit():

        new_ruche = Ruche(rucher=id, specie=form.breed.data, num=form.num.data, feedback=form.feedback.data)
        db.session.add(new_ruche)
        db.session.commit()

        return redirect(url_for('delete_rucher', id=id))    

    return render_template('rucher.html', ruches=rucher.get_ruches(), form=form)

@app.route('/add_ruche/<rucher_id>')
def add_ruche(rucher_id):
    form = RucheForm()
    if form.validate_on_submit():

        new_ruche = Ruche(rucher=rucher_id, specie=form.breed.data, num=form.num.data, feedback=form.feedback.data)
        db.session.add(new_ruche)
        db.session.commit()

        return redirect('/rucher/<id>')

    return render_template('add_ruche.html', form=form)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html')

if __name__ == '__main__':
    app.run(reload= True, debug=True)
