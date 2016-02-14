from flask import render_template, request
from weblog import app
from weblog.models import Visit

@app.route("/logs")
def logs():
    q = Visit.query
    type = request.args.get("type", "")
    value = request.args.get("value", "")
    if type in ["uri", "referral", "agent", "ip", "country"] and value != "":
        q = q.filter(getattr(Visit, type).like('%'+value+'%'))

    page = int(request.args.get("page", 1))
    logs = q.order_by("time desc").limit(25).offset(25*(page-1))
    maxpage = (q.count() // 25) + 1
    return render_template("logs.html", logs=logs, page=page, type=type, value=value, maxpage=maxpage)
