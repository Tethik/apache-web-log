from flask import Flask
import os
from flask.ext.bower import Bower

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
Bower(app)

import weblog.routes
