#!/usr/bin/python

from flask import render_template, session, redirect, url_for

from app.models import User, Manga, Chapter, Page, MangaBookmark
from app.scans import scans_bp
from app.scans.helpers import bookmark

@scans_bp.route("/")
def home():
    mangas = [ t[0] for t in Manga.query.with_entities(Manga.name).all() ]
    return render_template("scans/index.html", mangas=mangas)

@scans_bp.route("/<manga>")
def manga(manga):
    # if a bookmark is present, redirect the user to the last position directly
    try:
        current_user = User.query.filter_by(username=session['username']).first()
        if current_user:
            bookmark = MangaBookmark.query.filter_by(user_id=current_user.id, manga_name=manga).first()
            if bookmark:
                return redirect(url_for('scans_bp.page', manga=manga, chapter=bookmark.chapter, page=bookmark.page))
    except Exception as e:
        print(e)
    chapters = [ t[0] for t in Chapter.query.with_entities(Chapter.number).filter_by(manga_name=manga).all() ]
    return render_template("scans/manga.html", manga=manga, chapters=chapters)

@scans_bp.route("/<manga>/<chapter>")
def chapter(manga, chapter):
    # the bare chapter URL will redirect the user to page 1
    return redirect(url_for('scans_bp.page', manga=manga, chapter=chapter, page=1))

@scans_bp.route("/<manga>/<chapter>/<page>")
def page(manga, chapter, page):
    chapters = [ t[0] for t in Chapter.query.with_entities(Chapter.number).filter_by(manga_name=manga).all() ]
    pages = [ t[0] for t in Page.query.with_entities(Page.number).filter_by(manga_name=manga, chapter_number=chapter).all() ]
    path = Page.query.filter_by(manga_name=manga, chapter_number=chapter, number=page).first().path

    try:
        current_user = User.query.filter_by(username=session['username']).first()
        if current_user:
            bookmark(manga, chapter, page, current_user.id)
    except Exception as e:
        print(e)
    finally:
        return render_template("scans/page.html", manga=manga, chapters=chapters, pages=pages, chapter=chapter, page=int(page), path=path)
