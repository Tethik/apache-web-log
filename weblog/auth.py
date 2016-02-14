from flask import redirect, session
from functools import wraps

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not "logged_in" in session:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated
