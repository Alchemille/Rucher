import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False


"""

First focused on precomputations without restructuring to reduce number of operations with Alexandre P.
Experimented with different memory layout and loop ordering to improve locality. 
In particular, implemented the single contiguous array and the $(W, H, 3)$ layout.
Worked with Alexandre B. on vectorizing the code. 
In the vectorized code, worked on alignment of memory addresses and added FMAs where possible.



"""
