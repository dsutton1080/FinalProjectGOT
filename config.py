import os

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'GameOfThreads'
    FLASK_APP = os.environ.get('FLASK_APP') or 'main.py'