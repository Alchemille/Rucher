import os
basedir = os.path.abspath(os.path.dirname(__file__))
import flickr_api

flickr_api.set_keys(api_key = 'b653ceb7975ea0acb8fa1c941c692ae2', api_secret = '12c381d27a946845')

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

