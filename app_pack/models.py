from app_pack import db
import requests
import random
import os.path
import urllib.request
from flask import url_for
from googletrans import Translator


class Rucher(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    location = db.Column(db.String(64), index=True, unique=True)
    plants = db.Column(db.String(120))
    feedback = db.Column(db.Text)

    def get_url_image(self):

        filename = os.path.join(os.path.dirname(
            __file__), 'static', self.plants + '.jpg')

        # get cached image if exits
        if os.path.isfile(filename):
            return url_for('static', filename=self.plants + '.jpg')

        # request image from pixabay if no cached image
        translator = Translator()
        plant_en = translator.translate(self.plants)

        response = requests.get("https://pixabay.com/api/",
                                params={
                                    'key': '17026220-1aa33a59036a53ced9e61bee6',
                                    'q': plant_en.text + '+plant',
                                }
                                )
        hits = response.json()['hits']

        # return random flower image if no hit
        if not hits:
            response = requests.get("https://pixabay.com/api/",
                                    params={
                                        'key': '17026220-1aa33a59036a53ced9e61bee6',
                                        'q': 'bee+flower',
                                    }
                                    )
            hits = response.json()['hits']

        # cache resulting image
        URL = random.choice(hits)['imageURL']
        r = requests.get(URL)
        with open(filename, 'wb') as outfile:
            outfile.write(r.content)

        return URL

    def __repr__(self):
        return 'Rucher à {}'.format(self.location)


class Ruche(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    specie = db.Column(db.String(64), index=True)

    def __repr__(self):
        return 'Ruche {}'.format(id)
