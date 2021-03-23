#!/usr/bin/python

import pandas as pd
from flask import Blueprint, redirect, render_template, session, redirect, url_for, request, jsonify
from models import User, AnimeActivity
from extensions import db

from datetime import datetime

anime_bp = Blueprint('anime_bp', __name__, static_folder='static', static_url_path='anime', template_folder='templates')
df = pd.read_csv("anime/anime.csv")

@anime_bp.route("/")
def home():
    works = df.work.unique()
    return render_template("anime/index.html", works=works)

@anime_bp.route("/<work_id>")
def work(work_id):
    try:
        current_user = User.query.filter_by(username=session['username']).first()
        bookmark = AnimeActivity.query.filter_by(user_id=current_user.id, anime=work_id).order_by(AnimeActivity.updatetime.desc()).first()
        if bookmark:
            return redirect(url_for('anime_bp.episode', work_id=work_id, season_id=bookmark.season, episode_id=bookmark.episode))
    except Exception as e:
        print(e)
    seasons = df[df.work == work_id].season.sort_values().unique()
    return render_template("anime/work.html", work=work_id, seasons=seasons)

@anime_bp.route("/<work_id>/<season_id>")
def season(work_id, season_id):
    episodes = df[(df.work == work_id) & (df.season == season_id)].episode.sort_values()
    return render_template("anime/season.html", work=work_id, season=season_id, episodes=episodes)

@anime_bp.route("/<work_id>/<season_id>/<episode_id>")
def episode(work_id, season_id, episode_id):
    path = df[(df.work == work_id) & (df.season == season_id) & (df.episode == episode_id)].path.iloc[0]
    pos = 0
    try:
        current_user = User.query.filter_by(username=session['username']).first()
        bookmark = AnimeActivity.query.filter_by(user_id=current_user.id, anime=work_id, season=season_id, episode=episode_id).first()
        if bookmark:
            pos = bookmark.position
    except:
        print("Bad login") # logs ?
    finally:
        return render_template("anime/episode.html", work=work_id, season=season_id, episode=episode_id, path=f"anime/{path}", t=str(pos))

@anime_bp.route("/register_timestamp", methods=['POST'])
def register_timestamp():
    try:
        current_user = User.query.filter_by(username=session['username']).first()
        bookmark(request.form.get("work"), request.form.get("season"), request.form.get("episode"), current_user.id, pos=request.form.get("t"))
        print("bookmarked") # logs ?
    except:
        print("Bad login") # logs ?
    return jsonify(status="ok")

def bookmark(work_id, season_id, episode_id, user_id, pos=0):
    # check if a bookmark entry for this episode is present in the database
    db_bookmark = AnimeActivity.query.filter_by(user_id=user_id, anime=work_id, season=season_id, episode=episode_id).first()
    # update if present
    if db_bookmark:
        db_bookmark.season = season_id
        db_bookmark.episode = episode_id
        db_bookmark.position = pos
        db_bookmark.updatetime = datetime.now()
    # create if not
    else:
        new_bookmark = AnimeActivity(anime=work_id, season=season_id, episode=episode_id, user_id=user_id)
        db.session.add(new_bookmark)
    db.session.commit()
