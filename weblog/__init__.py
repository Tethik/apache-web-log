from flask import Flask
import os
from flask.ext.bower import Bower

app = Flask(__name__)
app.config.from_pyfile(os.getcwd() + "/config.cfg")
Bower(app)

import weblog.routes
