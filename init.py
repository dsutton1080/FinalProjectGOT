from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from stateless_functions import *

app = Flask(__name__)
Bootstrap(app)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'splash'

app.jinja_env.globals.update(grade_level_string = grade_level_string)
app.jinja_env.globals.update(state_abbrev_to_name = state_abbrev_to_name)

if not app.debug:
    import logging
    from logging.handlers import RotatingFileHandler
    handler = RotatingFileHandler('logs/website.log', 'a', 1 * 1024 * 1024, 10)
    handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    app.logger.setLevel(logging.INFO)
    handler.setLevel(logging.INFO)
    app.logger.addHandler(handler)
    app.logger.info('Logging Startup...')

import main, db_models