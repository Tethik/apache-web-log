from flask import Flask
import os

app = Flask(__name__)
app.config.from_pyfile(os.getcwd() + "/config.cfg")

import weblog.routes
