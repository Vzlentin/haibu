#!/usr/bin/python

from app import db

class Bookmarks(db.Model):
    work_id = db.Column(db.String(100), primary_key=True)
    mark = db.Column(db.String(10)
