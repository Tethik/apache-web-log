from weblog import app
import os

app.config.from_pyfile(os.getcwd() + "/config.cfg")

from weblog.models import db
db.create_all()
app.run(debug=True)
