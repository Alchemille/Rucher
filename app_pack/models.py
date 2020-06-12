from app_pack import db

class Rucher(db.Model):

    #__tablename__ = 'Ruchers' # by default, table name is rucher
    # possible contructor OR use db.Model
    
    id = db.Column(db.Integer, primary_key=True)
    location = db.Column(db.String(64), index=True, unique=True)
    plants = db.Column(db.String(120))
    feedback = db.Column(db.Text)

    def __repr__(self):
        return 'Rucher {} située à {}'.format(self.id, self.location)  

class Ruche(db.Model):

    #__tablename__ = 'Ruches' # by default, table name is ruche

    id = db.Column(db.Integer, primary_key=True)
    specie = db.Column(db.String(64), index=True)

    def __repr__(self):
        return 'Ruche {}'.format(id)