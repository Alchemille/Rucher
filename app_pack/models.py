from app_pack import db
import requests, random


class Rucher(db.Model):

    #__tablename__ = 'Ruchers' # by default, table name is rucher
    # possible contructor OR use db.Model
    
    id = db.Column(db.Integer, primary_key=True)
    location = db.Column(db.String(64), index=True, unique=True)
    plants = db.Column(db.String(120))
    feedback = db.Column(db.Text)

    def get_url_image(self):

        r = requests.get("https://api.qwant.com/api/search/images",
            params={
                'q': self.plants,
                't': 'images',
                'uiv': 4
            },
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
            }
        )

        response = r.json().get('data').get('result').get('items')
        urls = [r.get('media') for r in response]

        return random.choice(urls)

    def __repr__(self):
        return 'Rucher {} située à {}'.format(self.id, self.location)  

class Ruche(db.Model):

    #__tablename__ = 'Ruches' # by default, table name is ruche

    id = db.Column(db.Integer, primary_key=True)
    specie = db.Column(db.String(64), index=True)

    def __repr__(self):
        return 'Ruche {}'.format(id)