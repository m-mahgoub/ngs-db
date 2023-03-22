from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# source is a patient or cell line
class Source(db.Model):
    upn = db.Column(db.Integer, unique=True, primary_key=True)
    name = db.Column(db.String(64))
    age = db.Column(db.Integer)
    sex = db.Column(db.String(256))
    dx = db.Column(db.String(256))
    wbc = db.Column(db.Integer)
    pb_blast = db.Column(db.Integer)
    bm_blast = db.Column(db.Integer)
    karyotype = db.Column(db.String(256))
    fab = db.Column(db.String(256))
    yearbanked = db.Column(db.Integer)
    samples = db.relationship('Sample', backref='source', lazy=True)

    def to_dict(self):
        return {
            'upn': self.upn,
            'name': self.name,
            'age': self.age,
            'sex': self.sex,
            'dx': self.dx,
            'wbc': self.wbc,
            'pb_blast': self.pb_blast,
            'bm_blast': self.bm_blast,
            'karyotype': self.karyotype,
            'fab': self.fab,
            'yearbanked': self.yearbanked
        }
        
# sample from individual source (e.g blood, bone marrow, etc.)
class Sample(db.Model):
    usn = db.Column(db.Integer, unique=True, primary_key=True)
    upn = db.Column(db.Integer, db.ForeignKey('source.upn'))
    name = db.Column(db.String(64))
    type = db.Column(db.String(64))
    collectiondate = (db.Column(db.Date))
    time_point_weeks = db.Column(db.Integer)

    def to_dict(self):
        return {
            'usn': self.usn,
            'upn': self.upn,
            'name': self.name,
            'type': self.type,
            'collectiondate': self.collectiondate,
            'time_point_weeks': self.time_point_weeks
        }