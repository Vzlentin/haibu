#!/usr/bin/python

from extensions import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), index=True, unique=True)
    scan_activity = db.relationship('ScanActivity', backref='user', lazy=True)
    anime_activity = db.relationship('AnimeActivity', backref='user', lazy=True)

class ScanActivity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    manga = db.Column(db.String(100))
    chapter = db.Column(db.String(100))
    page = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class AnimeActivity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    updatetime = db.Column(db.DateTime)
    anime = db.Column(db.String(100))
    season = db.Column(db.String(100))
    episode = db.Column(db.String(100))
    position = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
