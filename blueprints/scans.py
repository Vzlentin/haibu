#!/usr/bin/python

import pandas as pd
from flask import Blueprint, render_template

scans_app = Blueprint("scans_app", __name__)
df = pd.read_csv("data/scans.csv")

@scans_app.route("/")
def home():
    works = df.work.unique()
    return render_template("scans/index.html", works=works)

@scans_app.route("/<work_id>")
def work(work_id):
    chapters = df[df.work == work_id].chap.sort_values().unique()
    return render_template("scans/work.html", work=work_id, chapters=chapters)

@scans_app.route("/<work_id>/<chapter_id>/<page_id>")
def page(work_id, chapter_id, page_id):
    chapters = df[df.work == work_id].chap.sort_values().unique()
    path = df[(df.work == work_id) & (df.chap == int(chapter_id)) & (df.page == int(page_id))].path.iloc[0]
    return render_template("scans/page.html", work=work_id, chapters=chapters, chapter=chapter_id, page=int(page_id), path=f"scans/{path}")
