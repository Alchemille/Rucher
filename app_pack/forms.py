from flask import Flask, render_template, session, redirect, url_for, session
from flask_wtf import FlaskForm
from wtforms import (StringField, BooleanField, DateTimeField,
                     RadioField,SelectField,TextField,
                     TextAreaField,SubmitField, PasswordField)
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo
from datetime import datetime
from app_pack import app, db
from app_pack.models import Rucher, Ruche, User

class RucherAddForm(FlaskForm):

    location = StringField("Emplacement",validators=[DataRequired()])
    plant = StringField("Plantes melliferes a proximite")
    lat = StringField("Latitude")
    longit = StringField("Longitude")
    feedback = TextAreaField()
    submit = SubmitField('Valider')

class RucheForm(FlaskForm):

    def check_rucher_exists(form, field):
        if not Rucher.query.get(field.data):
            raise ValidationError("Veuillez entrer un numéro de rucher valide")

    def check_espece_renseignee(form, field):
        if field.data == "other" and not form.new_breed.data:
            raise ValidationError("L'espece doit etre précisée") 

    def check_num_unique(form, field):
        q = db.session.query(
                User, Rucher, Ruche,
            ).filter(
                User.id == Rucher.user,
            ).filter(
                Rucher.id == Ruche.rucher,
            ).filter(
                Ruche.num == field.data,
            )      
        print(q.first())
        if q.first():
            raise ValidationError("La ruche {} existe déja".format(form.num.data))

    rucher = StringField("Rucher Parent")
    num = StringField("Numero",validators=[DataRequired(), check_num_unique, check_rucher_exists])
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

    def check_email_not_used(self,  field):
        if User.query.filter(User.email==field.data).first():
            raise ValidationError('Email déja utilisé')

    def check_name_not_used(self, field):
        if User.query.filter(User.email==field.data).first():
            raise ValidationError('Nom déja utilisé')

    name = StringField("Nom", validators=[DataRequired(), check_name_not_used])
    email = StringField("Email", validators=[DataRequired(), Email(message='Pas une adresse mail'), check_email_not_used])
    password = PasswordField('Mot de passe', validators=[DataRequired(), EqualTo('pass_confirm', message='Les mots de passe sont différents!')])
    pass_confirm = PasswordField('Confirmer mot de passe', validators=[DataRequired()])
    remember_me = BooleanField('Se souvenir de moi')
    submit = SubmitField("S'enregister")
