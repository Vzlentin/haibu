#!/usr/bin/python

from extensions import db
from app.models import Manga, MangaBookmark

def bookmark(manga, chapter, page, user_id):
    # check if a bookmark entry for this manga is present in the database
    manga_id = Manga.query.filter_by(name=manga).first().id
    db_bookmark = MangaBookmark.query.filter_by(user_id=user_id, manga_name=manga).first()
    # update if present
    if db_bookmark:
        db_bookmark.chapter = chapter
        db_bookmark.page = page
    # create if not
    else:
        new_bookmark = MangaBookmark(manga_id=manga_id, manga_name=manga, chapter=chapter, page=page, user_id=user_id)
        db.session.add(new_bookmark)
    db.session.commit()
