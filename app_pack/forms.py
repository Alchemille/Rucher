from flask import Flask, render_template, session, redirect, url_for, session
from flask_wtf import FlaskForm
from wtforms import (StringField, BooleanField, DateTimeField,
                     RadioField,SelectField,TextField,
                     TextAreaField,SubmitField, PasswordField)
from wtforms.validators import DataRequired


class RucherAddForm(FlaskForm):

    location = StringField("Emplacement",validators=[DataRequired()])
    plant = StringField("Plantes melliferes a proximite")
    lat = StringField("Latitude")
    longit = StringField("Longitude")
    feedback = TextAreaField()
    submit = SubmitField('Valider')

class RucheForm(FlaskForm):

    num = StringField("Numero",validators=[DataRequired()])
    breed = RadioField("Espece actuelle", choices = [('bugfast', 'bugfast'), ('caucasienne', 'caucasienne'), ('autre', 'autre')], validators=[DataRequired()])
    #rucher = StringField("Rucher parent", validators=[DataRequired()])
    #queen = StringField("Reine")
    feedback = TextAreaField()
    submit = SubmitField('Valider')

class LoginForm(FlaskForm):
    name = StringField("Votre Nom")
    password = PasswordField('Entrer le mot de passe', validators=[DataRequired()])
    remember_me = BooleanField('Se souvenir de moi')
    submit = SubmitField('Valider')