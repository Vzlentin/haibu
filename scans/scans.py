#!/usr/bin/python

import pandas as pd
from flask import Blueprint, render_template, session, redirect, url_for
from models import User, ScanActivity
from extensions import db

scans_bp = Blueprint("scans_bp", __name__, static_folder='static', static_url_path='scans', template_folder='templates')
df = pd.read_csv("scans/scans.csv")

@scans_bp.route("/")
def home():
    works = df.work.unique()
    return render_template("scans/index.html", works=works)

@scans_bp.route("/<work_id>")
def work(work_id):
    # if a bookmark is present, redirect the user to the last position directly
    try:
        current_user = User.query.filter_by(username=session['username']).first()
        bookmark = ScanActivity.query.filter_by(user_id=current_user.id, manga=work_id).first()
        if bookmark:
            return redirect(url_for('scans_bp.page', work_id=work_id, chapter_id=bookmark.chapter, page_id=bookmark.page))
    except Exception as e:
        print(e)
    chapters = df[df.work == work_id].chap.sort_values().unique()
    return render_template("scans/work.html", work=work_id, chapters=chapters)

@scans_bp.route("/<work_id>/<chapter_id>")
def chapter(work_id, chapter_id):
    # the bare chapter URL will redirect the user to page 1
    return redirect(url_for('scans_bp.page', work_id=work_id, chapter_id=chapter_id, page_id=1))

@scans_bp.route("/<work_id>/<chapter_id>/<page_id>")
def page(work_id, chapter_id, page_id):
    chapters = df[df.work == work_id].chap.sort_values().unique()
    pages = df[(df.work == work_id) & (df.chap == int(chapter_id))].page.sort_values()
    path = df[(df.work == work_id) & (df.chap == int(chapter_id)) & (df.page == int(page_id))].path.iloc[0]
    try:
        current_user = User.query.filter_by(username=session['username']).first()
        bookmark(work_id, chapter_id, page_id, current_user.id)
    except:
        print("Bad login") # logs ?
    finally:
        return render_template("scans/page.html", work=work_id, chapters=chapters, pages=pages, chapter=chapter_id, page=int(page_id), path=f"scans/{path}")

def bookmark(work_id, chapter_id, page_id, user_id):
    # check if a bookmark entry for this manga is present in the database
    db_bookmark = ScanActivity.query.filter_by(user_id=user_id, manga=work_id).first()
    # update if present
    if db_bookmark:
        db_bookmark.chapter = chapter_id
        db_bookmark.page = page_id
    # create if not
    else:
        new_bookmark = ScanActivity(manga=work_id, chapter=chapter_id, page=page_id, user_id=user_id)
        db.session.add(new_bookmark)
    db.session.commit()
