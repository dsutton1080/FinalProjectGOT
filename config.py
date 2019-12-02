import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    """
    This class defines common global configuration options of the Flask application.
    Inherits from an object type.
    """
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'GameOfThreads'
    FLASK_APP = os.environ.get('FLASK_APP') or 'main.py'
    TEST_USER_POPULATED_DB = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'dev2.db') \
                               if TEST_USER_POPULATED_DB \
                               else os.environ.get('DATABASE_URL') or \
                                    'sqlite:///' + os.path.join(basedir, 'dev.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    ELASTICSEARCH_URL = os.environ.get('ELASTICSEARCH_URL') or 'http://localhost:9200'
