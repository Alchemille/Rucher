from flask import Flask, render_template, session, redirect, url_for, session, flash
from flask_wtf import FlaskForm
from wtforms import (StringField, BooleanField, DateTimeField,
                     RadioField,SelectField,TextField,
                     TextAreaField,SubmitField)

from wtforms.validators import DataRequired
from app_pack.forms import *

from app_pack import app, db
from app_pack.models import Rucher
from flickr_api import Photo, Walker

import requests, random
from werkzeug.exceptions import NotFound                     


"""
default static route : https://stackoverflow.com/questions/20646822/how-to-serve-static-files-in-flask
"""

@app.route('/')
def index():

    ruchers = Rucher.query.all()

    return render_template('ruchers.html', ruchers=ruchers)

@app.route('/add_rucher', methods=['GET', 'POST'])
def add_rucher():

    form = RucherAddForm()
    if form.validate_on_submit():

        new_rucher = Rucher(location=form.location.data, plants=form.plant.data, feedback=form.feedback.data)
        db.session.add(new_rucher)
        db.session.commit()

        flash('Rucher {} ajouté'.format(form.location.data))

        return redirect('/')

    return render_template('add_rucher.html', form=form)

@app.route('/delete_rucher/<id>', methods=['POST'])      
def delete_rucher(id):
    db.session.delete(Rucher.query.get(id))
    db.session.commit()
    return redirect('/')

@app.route('/rucher/<id>')
def see_rucher(id):

    # source : https://jereze.com/code/image-search-api/

    rucher = Rucher.query.get(id)

    if not rucher:
        raise NotFound

    query = rucher.plants

    r = requests.get("https://api.qwant.com/api/search/images",
        params={
            'q': query,
            't': 'images',
            'uiv': 4
        },
        headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
        }
    )

    response = r.json().get('data').get('result').get('items')
    urls = [r.get('media') for r in response]

    return redirect(random.choice(urls))

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html')

@app.route('/login', methods=['GET', 'POST'])
def login():

    form = LoginForm()
    if form.validate_on_submit() and form.password.data == 'billy':

        flash('Login requested for user {}, remember_me={}'.format(
            form.name.data, form.remember_me.data)) # appear only once
        # or use session in template rendering in thankyou/
        return redirect(url_for("merci"))
        # or redirect("/thankyou")

    return render_template('login.html', form=form)


@app.route('/thankyou')
def merci():

    return render_template('merci.html')


if __name__ == '__main__':
    app.run(reload= True, debug=True)
