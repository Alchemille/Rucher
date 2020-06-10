from flask import Flask, render_template, session, redirect, url_for, session, flash
from flask_wtf import FlaskForm
from wtforms import (StringField, BooleanField, DateTimeField,
                     RadioField,SelectField,TextField,
                     TextAreaField,SubmitField)
from wtforms.validators import DataRequired
from app_pack.forms import *

from app_pack import app

app.config['SECRET_KEY'] = 'mysecretkey'

@app.route('/', methods=['GET', 'POST'])
def index():

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
