#!/usr/bin/python

from datetime import datetime

from extensions import db
from app.models import Anime, AnimeBookmark

def bookmark(anime, season, episode, user_id, pos=0):
    # check if a bookmark entry for this episode is present in the database
    anime_id = Anime.query.filter_by(name=anime).first().id
    db_bookmark = AnimeBookmark.query.filter_by(user_id=user_id, anime_name=anime, season=season, episode=episode).first()
    # update if present
    if db_bookmark:
        db_bookmark.season = season
        db_bookmark.episode = episode
        db_bookmark.position = pos
        db_bookmark.updatetime = datetime.now()
    # create if not
    else:
        new_bookmark = AnimeBookmark(updatetime=datetime.now(), anime_id=anime_id, anime_name=anime, season=season, episode=episode, position=pos, user_id=user_id)
        db.session.add(new_bookmark)
    db.session.commit()
