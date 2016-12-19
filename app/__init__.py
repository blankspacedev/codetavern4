from flask import Flask
from flask_script import Manager
from flask_bootstrap import Bootstrap
import requests, base64, json



app = Flask(__name__)
app.config['DEBUG']=True

manager = Manager(app)
bootstrap = Bootstrap(app)

from .views import *
