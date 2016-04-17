from flask import render_template, redirect, session, send_from_directory
from weblog import app

@app.route("/")
def start():
    if not "logged_in" in session:
        return redirect("/login")
    return redirect("/dashboard/weekly")

import weblog.routes.login
import weblog.routes.dashboard
import weblog.routes.logs

@app.route('/<path:path>')
def static_stuff(path):
    return app.send_static_file(path)
