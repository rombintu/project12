import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

from project import config

app = Flask(__name__)
# app.config.from_object(os.environ['APP_SETTINGS'])
app.config.from_object(config.Config)
# app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
manager = LoginManager(app)

from project import models, routes


db.create_all()

