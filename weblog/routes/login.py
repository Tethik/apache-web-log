from flask import request, render_template, session, redirect
from weblog import app
from weblog.auth import requires_auth
from passlib.hash import sha256_crypt
from weblog.models import Setting

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        password = request.form["password"]

        if not check_auth(password):
            return render_template("login.html", msg="Try again.")

        # login and validate the user...
        session['logged_in'] = "yep"

        return redirect(request.args.get("next") or "/")
    return render_template("login.html")

@app.route("/logout")
@requires_auth
def logout():
    del session['logged_in']
    return redirect("/login")

def check_auth(password):
    pw = app.config['PASSWORD']
    if len(password) != len(pw):
        return False
    result = 0
    for x, y in zip(password, pw):
        result |= ord(x) ^ ord(y)
    return result == 0
