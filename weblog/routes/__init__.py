from flask import render_template, redirect, session
from weblog import app

@app.route("/")
def start():
    if not "logged_in" in session:
        return redirect("/login")
    return redirect("/dashboard/weekly")

import weblog.routes.login
import weblog.routes.dashboard
import weblog.routes.logs
