from flask import render_template
from weblog import app

@app.route("/")
def index():
    return render_template("index.html")

import weblog.routes.logs
