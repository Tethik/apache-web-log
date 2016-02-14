from __future__ import division
from flask import render_template, redirect
from weblog import app
from datetime import datetime, timedelta
from weblog.models import Visit
import json


@app.route("/dashboard/")
def dashboard_default():
    return redirect("/dashboard/weekly")

@app.route("/dashboard/<time>")
def dashboard(time):
    pages = []
    page = { "title": "merp", "count": 1322 }
    pages.append(page)
    d = _data(time)
    return render_template("dashboard.html",
        time_period=time,
        visited_pages=_visited_pages(d),
        countries=_countries(d),
        # unique_visitors_data=_unique_visitors(d, time),
        page_views_data=_page_views(d, time))

def _time_period(s):
    end = datetime.now()
    options = {
        "daily": end - timedelta(days=1),
        "weekly": end - timedelta(days=7),
        "monthly": end - timedelta(days=30),
        "year": end - timedelta(days=365)
    }
    return options.get(s, options["weekly"]), end

def _data(s):
    start, end = _time_period(s)
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
    # k = int(dt.hour)
    v = str(datetime(year=1970, month=1, day=1, hour=dt.hour))
    return k,v

def _day_km(dt):
    # Indexed by day
    k = v = str(datetime(year=dt.year, month=dt.month, day=dt.day))
    return k,v

def _month_km(dt):
    # Indexed by month
    k = v = str(datetime(year=dt.year, month=dt.month, day=1))
    return k,v


# def _unique_visitors(data, time_period):
#     return json.dumps(_uv_day(data))

# def _uv_day(data):
#     # 24 hour period
#     rows = []
#     grp = {}
#     now = datetime.now()
#     for row in data:
#         h = int(row.time.hour)
#         if not h in grp:
#             grp[h] = { "x": str(datetime(year=now.year, month=now.month, day=now.day, hour=h)), "visitors": 0 }
#             rows.append(grp[h])
#         grp[h]["visitors"] += 1
#         # rows.append({ "x": str(row.time), "visitors": 1 })
#
#     return rows

def _page_views(data, time_period):
    grp_functions = {
        "daily": _hour_km,
        "weekly": _day_km,
        "monthly": _day_km,
        "year": _month_km
    }

    f = grp_functions.get(time_period, _day_km)

    # 24 hour period
    rows = []
    grp = {}
    now = datetime.now()
    for row in data:
        k, v = f(row.time)
        if not k in grp:
            grp[k] = { "x": k, "views": 0, "unique": set() }
            rows.append(grp[k])
        grp[k]["views"] += 1
        grp[k]["unique"].add(row.ip)
        # rows.append({ "x": str(row.time), "visitors": 1 })

    for k in grp:
        grp[k]["unique_count"] = len(grp[k]["unique"])
        del grp[k]["unique"]


    return json.dumps(rows)
