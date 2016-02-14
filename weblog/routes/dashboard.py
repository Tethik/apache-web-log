from __future__ import division
from flask import render_template, redirect
from weblog import app
from weblog.auth import requires_auth
from datetime import datetime, timedelta
from weblog.models import Visit
import json

@app.route("/dashboard/")
@requires_auth
def dashboard_default():
    return redirect("/dashboard/weekly")

@app.route("/dashboard/<time>")
@requires_auth
def dashboard(time):
    pages = []
    page = { "title": "merp", "count": 1322 }
    pages.append(page)
    start, end = _time_period(time)
    d = _data(start, end)
    return render_template("dashboard.html",
        time_period=time,
        visited_pages=_visited_pages(d),
        countries=_countries(d),
        # unique_visitors_data=_unique_visitors(d, time),
        page_views_data=_page_views(d, time, start, end))

def _time_period(s):
    end = datetime.now()
    options = {
        "daily": end - timedelta(days=1),
        "weekly": end - timedelta(days=7),
        "monthly": end - timedelta(days=30),
        "year": end - timedelta(days=365)
    }
    return options.get(s, options["weekly"]), end

def _data(start, end):
    q = Visit.query.filter(Visit.time >= start, Visit.time <= end).all()
    return q

def _clean_uri(uri):
    i = uri.find("?")
    return uri[:i] if i > -1 else uri

def _visited_pages(data):
    pages = []
    grp = {}
    for row in data:
        u = _clean_uri(row.uri)
        if u.endswith(".css") or u.endswith(".png"):
            continue

        if row.status_code == "404":
            continue

        if not u in grp:
            r = { "title": u, "count": 0 }
            grp[u] = r
            pages.append(r)
        grp[u]["count"] = grp[u]["count"] + 1
    return sorted(pages, key=lambda x: -x["count"])[:10]

def _countries(data):
    pages = []
    grp = {}
    total = len(data)
    for row in data:
        # if "bot" in row.agent.lower() or "baidu" in row.agent.lower():
        #     continue

        if not row.country in grp:
            r = { "name": row.country, "count": 0, "percent": 0.0 }
            grp[row.country] = r
            pages.append(r)
        grp[row.country]["count"] += 1
        grp[row.country]["percent"] = "{0:.2f}".format(grp[row.country]["count"] / total * 100.0)

    return sorted(pages, key=lambda x: -x["count"])[:10]

def _hour_km(dt):
    # Indexed by 24 hour
    k = v = str(datetime(year=1970, month=1, day=1, hour=dt.hour))
    return k,v

def _day_km(dt):
    # Indexed by day
    k = v = str(datetime(year=dt.year, month=dt.month, day=dt.day))
    return k,v

def _month_km(dt):
    # Indexed by month
    k = v = str(datetime(year=dt.year, month=dt.month, day=1))
    return k,v

def _hour_keys(start, end):
    return [str(datetime(year=1970, month=1, day=1, hour=i)) for i in xrange(24)]

def _day_keys(start, end):
    days = []
    curr = datetime(year=start.year, month=start.month, day=start.day)
    while curr <= end:
        days.append(str(curr))
        curr += timedelta(days=1)
    return days

def _month_keys(start, end):
    days = []
    curr = datetime(year=start.year, month=start.month, day=1)
    while curr <= end:
        days.append(str(curr))
        m = curr.month + 1
        y = curr.year
        if m > 12:
            y += 1
            m = 1
        curr = datetime(year=y, month=m, day=1)

    return days

def _page_views(data, time_period, start, end):
    grp_functions = {
        "daily": (_hour_km, _hour_keys),
        "weekly": (_day_km, _day_keys),
        "monthly": (_day_km, _day_keys),
        "year": (_month_km, _month_keys)
    }

    f, keygen = grp_functions.get(time_period, _day_km)

    # 24 hour period
    rows = []
    grp = {}

    for k in keygen(start, end):
        grp[k] = { "x": str(k), "views": 0, "unique": set() }
        rows.append(grp[k])

    for row in data:
        k, v = f(row.time)
        grp[k]["views"] += 1
        grp[k]["unique"].add(row.ip)

    # Could be optimized to not save all these sets.
    for k in grp:
        grp[k]["unique_count"] = len(grp[k]["unique"])
        del grp[k]["unique"]


    return json.dumps(rows)
