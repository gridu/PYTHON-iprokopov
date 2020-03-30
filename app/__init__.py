from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_iniconfig import INIConfig
import logging
import os


app = Flask(__name__)
INIConfig(app)
app.config.from_inifile(f"{os.path.dirname(os.path.realpath(__file__))}/config/config.ini")

logging_subdir = (app.config.get('logging') or {}).get('logs_subdirectory_name')
logging_file = (app.config.get('logging') or {}).get('log_file_name')

logs_dir = f"{os.path.dirname(os.path.realpath(__file__))}/{logging_subdir}"

if not os.path.exists(logs_dir):
    os.mkdir(logs_dir)

logging.basicConfig(filename=f"{logs_dir}/{logging_file}", level=logging.INFO,
                    format='%(asctime)s: %(levelname)s: %(message)s')


app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = (app.config.get('sqlalchemy') or {}).get('track_modifications')
app.config['SQLALCHEMY_DATABASE_URI'] = (app.config.get('sqlalchemy') or {}).get('database_uri')
app.config['SECRET_KEY'] = (app.config.get('jwt') or {}).get('secret_key')
app.config['JWT_AUTH_USERNAME_KEY'] = (app.config.get('jwt') or {}).get('username_key')
app.config['JWT_AUTH_PASSWORD_KEY'] = (app.config.get('jwt') or {}).get('password_key')
app.config['JWT_AUTH_URL_RULE'] = (app.config.get('jwt') or {}).get('auth_url_rule')

db = SQLAlchemy(app)

from .app import *
