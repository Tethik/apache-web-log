from weblog import app
from weblog.models import db
import os

db.create_all()
app.run(debug=True)
