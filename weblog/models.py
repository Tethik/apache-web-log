from weblog import app
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy(app)

class Visit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.DateTime)
    status_code = db.Column(db.String(250))
    uri = db.Column(db.String(250))
    referral = db.Column(db.String(250))
    agent = db.Column(db.String(250))
    ip = db.Column(db.String(250))
    country = db.Column(db.String(2))

    def to_json(self):
        return dict(id=self.id,
            time=self.time,
            status_code=self.status_code,
            uri=self.uri,
            referral=self.referral,
            agent=self.agent,
            ip=self.ip,
            country=self.country
        )

class Setting(db.Model):
    key = db.Column(db.String, primary_key=True)
    value = db.Column(db.String)

    @staticmethod
    def get(key):
        o = Setting.query.filter(Setting.key == key).first()
        return o.value if o else None

    @staticmethod
    def set(key, value):
        o = Setting.query.filter(Setting.key == key).first()
        if not o:
            o = Setting(key = key)
        o.value = value
        db.session.add(o)
        db.session.commit()
