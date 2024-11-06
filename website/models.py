from website import db
from flask_login import UserMixin
from sqlalchemy.sql import func 
from datetime import datetime

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(10000), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    date_created = datetime.now()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    email = db.Column(db.String(120), unique=True, index=True)
    password_hash = db.Column(db.String(150))
    notes = db.relationship('Note', backref='user', lazy='dynamic')

