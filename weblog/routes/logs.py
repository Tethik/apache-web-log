from flask import render_template, request
from weblog import app
from weblog.models import Visit

@app.route("/logs")
def logs():
    page = request.args.get("page", 0)

    logs = Visit.query.limit(25).offset(25*page)
    return render_template("logs.html", logs=logs)
