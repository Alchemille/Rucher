from flask import Flask, render_template, session, redirect, url_for, session
from flask_wtf import FlaskForm
from wtforms import (StringField, BooleanField, DateTimeField, IntegerField,
                     RadioField,SelectField,TextField,
                     TextAreaField,SubmitField, PasswordField)
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo
from datetime import datetime
from app_pack import app, db
from app_pack.models import Rucher, Ruche, User
from flask_login import current_user

class RucherAddForm(FlaskForm):

    location = StringField("Nom du rucher",validators=[DataRequired()])
    plants = StringField("Plantes melliferes a proximite")
    lat = StringField("Latitude")
    longit = StringField("Longitude")
    feedback = TextAreaField()
    submit = SubmitField('Valider')

class RucheForm(FlaskForm):

    def check_espece_renseignee(form, field):
        if field.data == "other" and not form.specie.data:
            raise ValidationError("L'espece doit etre précisée") 

    def check_num_unique(form, field):
        q = db.session.query(
                Ruche,
            ).filter(
                Ruche.user == current_user.id,
            ).filter(
                Ruche.num == field.data,
            )      
        print(q.first())
        if q.first():
            raise ValidationError("La ruche {} existe déja".format(form.num.data))

    rucher = SelectField("Rucher Parent", coerce=int)
    num = IntegerField("Numero",validators=[DataRequired(), check_num_unique])
    specie_select = SelectField("Espece actuelle", default="other", validators=[check_espece_renseignee])
    specie = StringField("Si autre, quelle espece?")
    age_reine = DateTimeField("Date de naissance de la reine", default=datetime.today(), format="%d/%m/%y")
    feedback = TextAreaField("Autres caractéristiques")
    submit = SubmitField('Valider')

class EventForm(FlaskForm):

    def check_type_defined(form, field):
        if form.type_select.data=="other" and not form.type.data:
            raise ValidationError("Le type d'éventement doit etre renseigné")


    def check_ruche_exists_allowed(form, field):
        ruche = Ruche.query.filter_by(user=current_user.id, num=field.data).all()
        if not ruche:
            raise ValidationError("Vous ne possédez pas cette ruche")

    ruche = IntegerField('Ruche', validators=[DataRequired(), check_ruche_exists_allowed])
    timestamp = DateTimeField("Date de l'évenement", default=datetime.today(), format="%d/%m/%y")
    type_select = SelectField("Type d'évenement")
    type = StringField("Si autre, lequel?", validators=[check_type_defined])
    note = TextAreaField("Remarques")
    submit = SubmitField("Valider")

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Mot de passe', validators=[DataRequired()])
    remember_me = BooleanField("Se souvenir de moi")
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
