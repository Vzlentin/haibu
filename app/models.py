#!/usr/bin/python

from extensions import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), index=True, unique=True)
    manga_bookmarks = db.relationship('MangaBookmark', backref='user', lazy=True)
    anime_bookmarks = db.relationship('AnimeBookmark', backref='user', lazy=True)

class Manga(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    chapters = db.relationship('Chapter', backref='manga', lazy=True)

class Chapter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.Integer)
    manga_id = db.Column(db.Integer, db.ForeignKey('manga.id'))
    manga_name = db.Column(db.String(100))
    pages = db.relationship('Page', backref='manga', lazy=True)

class Page(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.Integer)
    manga_id = db.Column(db.Integer)
    manga_name = db.Column(db.String(100))
    chapter_id = db.Column(db.Integer, db.ForeignKey('chapter.id'))
    chapter_number = db.Column(db.Integer)
    path = db.Column(db.String(100))

class MangaBookmark(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    manga_id = db.Column(db.Integer)
    manga_name = db.Column(db.String(100))
    chapter = db.Column(db.Integer)
    page = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class Anime(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    seasons = db.relationship('Season', backref='anime', lazy=True)

class Season(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    anime_id = db.Column(db.Integer, db.ForeignKey('anime.id'))
    anime_name = db.Column(db.String(100))
    episodes = db.relationship('Episode', backref='anime', lazy=True)

class Episode(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    anime_id = db.Column(db.Integer)
    anime_name = db.Column(db.String(100))
    season_id = db.Column(db.Integer, db.ForeignKey('season.id'))
    season_name = db.Column(db.String(100))
    path = db.Column(db.String(100))

class AnimeBookmark(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    updatetime = db.Column(db.DateTime)
    anime_id = db.Column(db.Integer)
    anime_name = db.Column(db.String(100))
    season = db.Column(db.String(100))
    episode = db.Column(db.String(100))
    position = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
