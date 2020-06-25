from flask import Flask, render_template, session, redirect, url_for, session
from flask_wtf import FlaskForm
from wtforms import (StringField, BooleanField, DateTimeField,
                     RadioField,SelectField,TextField,
                     TextAreaField,SubmitField, PasswordField)
from wtforms.validators import DataRequired, ValidationError


class RucherAddForm(FlaskForm):

    location = StringField("Emplacement",validators=[DataRequired()])
    plant = StringField("Plantes melliferes a proximite")
    lat = StringField("Latitude")
    longit = StringField("Longitude")
    feedback = TextAreaField()
    submit = SubmitField('Valider')

class RucheForm(FlaskForm):

    def check_espece_renseignee(form, field):
        print(field.data, form.new_breed.data)
        if field.data == "other" and not form.new_breed.data:
            raise ValidationError("L'espece doit etre précisée") 


    num = StringField("Numero",validators=[DataRequired()])
    breed = SelectField("Espece actuelle", validators=[DataRequired(), check_espece_renseignee])
    new_breed = StringField("Si autre, quelle espece?")
    feedback = TextAreaField()
    submit = SubmitField('Valider')


class LoginForm(FlaskForm):
    name = StringField("Votre Nom")
    password = PasswordField('Entrer le mot de passe', validators=[DataRequired()])
    remember_me = BooleanField('Se souvenir de moi')
    submit = SubmitField('Valider')