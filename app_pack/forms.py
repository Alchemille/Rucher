from flask import Flask, render_template, session, redirect, url_for, session
from flask_wtf import FlaskForm
from wtforms import (StringField, BooleanField, DateTimeField,
                     RadioField,SelectField,TextField,
                     TextAreaField,SubmitField, PasswordField)
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo
from datetime import datetime

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

    rucher = StringField("Rucher Parent")
    num = StringField("Numero",validators=[DataRequired()])
    breed = SelectField("Espece actuelle", validators=[check_espece_renseignee])
    new_breed = StringField("Si autre, quelle espece?")
    age_queen = DateTimeField("Date de naissance de la reine", default=datetime.today(), format='%d/%m/%y')
    feedback = TextAreaField("Autres caractéristiques")
    submit = SubmitField('Valider')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Mot de passe', validators=[DataRequired()])
    submit = SubmitField('Connexion')


class RegistrationForm(FlaskForm):
    name = StringField("Nom", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField('Mot de passe', validators=[DataRequired(), EqualTo('pass_confirm', message='Les mots de passe sont différents!')])
    pass_confirm = PasswordField('Confirmer mot de passe', validators=[DataRequired()])
    remember_me = BooleanField('Se souvenir de moi')
    submit = SubmitField('Se connecter')

    def check_email_not_used(self,  field):
        if User.query.filter(email=field.data).first():
            raise ValidationError('Email déja utilisé')

    def check_name_not_used(self, field):
        if User.query.filter(email=field.data).first():
            raise ValidationError('Nom déja utilisé')