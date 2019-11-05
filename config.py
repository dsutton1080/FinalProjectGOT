import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    """
    This class defines common global configuration options in the form of environment variables.
    """
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'GameOfThreads'
    FLASK_APP = os.environ.get('FLASK_APP') or 'main.py'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False