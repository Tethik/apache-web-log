from flask import render_template, redirect
from weblog import app

@app.route("/")
def start():
    return redirect("/dashboard/weekly")


import weblog.routes.dashboard
import weblog.routes.logs
