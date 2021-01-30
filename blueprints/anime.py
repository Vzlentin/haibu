#!/usr/bin/python

import pandas as pd
from flask import Blueprint, redirect, render_template

anime_app = Blueprint('anime_app', __name__)
df = pd.read_csv("data/anime.csv")

@anime_app.route("/")
def home():
    works = df.work.unique()
    return render_template("anime/index.html", works=works)

@anime_app.route("/<work_id>")
def work(work_id):
    seasons = df[df.work == work_id].season.sort_values().unique()
    return render_template("anime/work.html", work=work_id, seasons=seasons)

@anime_app.route("/<work_id>/<season_id>")
def season(work_id, season_id):
    episodes = df[(df.work == work_id) & (df.season == season_id)].episode.sort_values()
    return render_template("anime/season.html", work=work_id, season=season_id, episodes=episodes)

@anime_app.route("/<work_id>/<season_id>/<episode_id>")
def episode(work_id, season_id, episode_id):
    path = df[(df.work == work_id) & (df.season == season_id) & (df.episode == episode_id)].path.iloc[0]
    try:
        return redirect(f"/static/anime/{path}")
    except:
        print("Request aborted")
