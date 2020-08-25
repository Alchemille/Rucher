from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy import MetaData
from flask_login import LoginManager
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_repr import RepresentableBase

login_manager = LoginManager()

naming_convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(column_0_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app, model_class=RepresentableBase, metadata=MetaData(naming_convention=naming_convention))
migrate = Migrate(app, db)

login_manager.init_app(app)
login_manager.login_view = 'login' # redirection to 'login.html' when decorator @login_required not satisfied

from app_pack import routes, models

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': models.User, 'Rucher': models.Rucher, 'Ruche': models.Ruche}