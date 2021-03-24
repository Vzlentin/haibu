#!/usr/bin/python

from flask import redirect, render_template, session, redirect, url_for, request, jsonify

from app.models import User, Anime, Season, Episode, AnimeBookmark
from app.anime import anime_bp
from app.anime.helpers import bookmark

@anime_bp.route("/")
def home():
    animes = [ t[0] for t in Anime.query.with_entities(Anime.name).all() ]
    return render_template("anime/index.html", animes=animes)

@anime_bp.route("/<anime>")
def anime(anime):
    try:
        current_user = User.query.filter_by(username=session['username']).first()
        if current_user:
            bookmark = AnimeBookmark.query.filter_by(user_id=current_user.id, anime_name=anime).order_by(AnimeBookmark.updatetime.desc()).first()
            if bookmark:
                return redirect(url_for('anime_bp.episode', anime=anime, season=bookmark.season, episode=bookmark.episode))
    except Exception as e:
        print(e)
    seasons = [ t[0] for t in Season.query.with_entities(Season.name).filter_by(anime_name=anime).all() ]
    return render_template("anime/anime.html", anime=anime, seasons=seasons)

@anime_bp.route("/<anime>/<season>")
def season(anime, season):
    episodes = [ t[0] for t in Episode.query.with_entities(Episode.name).filter_by(anime_name=anime, season_name=season).all() ]
    return render_template("anime/season.html", anime=anime, season=season, episodes=episodes)

@anime_bp.route("/<anime>/<season>/<episode>")
def episode(anime, season, episode):
    path = Episode.query.filter_by(anime_name=anime, season_name=season, name=episode).first().path
    pos = 0
    try:
        current_user = User.query.filter_by(username=session['username']).first()
        if current_user:
            bookmark = AnimeBookmark.query.filter_by(user_id=current_user.id, anime_name=anime, season=season, episode=episode).first()
            if bookmark:
                pos = bookmark.position
    except Exception as e:
        print(e)
    finally:
        return render_template("anime/episode.html", anime=anime, season=season, episode=episode, path=path, t=str(pos))

@anime_bp.route("/register_timestamp", methods=['POST'])
def register_timestamp():
    try:
        current_user = User.query.filter_by(username=session['username']).first()
        if current_user:
            bookmark(request.form.get("anime"), request.form.get("season"), request.form.get("episode"), current_user.id, pos=request.form.get("t"))
    except Exception as e:
        print(e)
    return jsonify(status="ok")
