#!/usr/bin/python

from flask import render_template, session, redirect, url_for

from app.models import User, Manga, Chapter, Page, MangaBookmark
from app.scans import scans_bp
from app.scans.helpers import bookmark

@scans_bp.route("/")
def home():
    mangas = [t[0] for t in Manga.query.with_entities(Manga.name).all()]
    return render_template("scans/index.html", mangas=mangas)

@scans_bp.route("/<m>")
def manga(m):
    # if a bookmark is present, redirect the user to the last position directly
    try:
        current_user = User.query.filter_by(username=session['username']).first()
        if current_user:
            bookmark = MangaBookmark.query.filter_by(user_id=current_user.id, manga_name=manga).first()
            if bookmark:
                return redirect(url_for('scans_bp.page', m=m, c=bookmark.chapter, p=bookmark.page))
    except Exception as e:
        print(e)
    chapters = [t[0] for t in Chapter.query.with_entities(Chapter.number).filter_by(manga_name=m).all()]
    return render_template("scans/manga.html", m=m, chapters=chapters)

@scans_bp.route("/<m>/<c>")
def chapter(m, c):
    # the bare chapter URL will redirect the user to page 1
    return redirect(url_for('scans_bp.page', m=m, c=int(c), p=1))

@scans_bp.route("/<m>/<c>/<p>")
def page(m, c, p):
    c = int(c)
    p = int(p)
    chapters = [t[0] for t in Chapter.query.with_entities(Chapter.number).filter_by(manga_name=m).all()]
    pages = [t[0] for t in Page.query.with_entities(Page.number).filter_by(manga_name=m, chapter_number=c).all()]

    if p > len(pages):
        return redirect(url_for('scans_bp.page', m=m, c=c+1, p=1))
    elif p < 1:
        prev_chap = Chapter.query.filter_by(number=c-1).first()
        last_page_number = [t[0] for t in Page.query.with_entities(Page.number).filter_by(manga_name=m, chapter_number=prev_chap.number).all()][-1]
        return redirect(url_for('scans_bp.page', m=m, c=prev_chap.number, p=last_page_number))

    path = Page.query.filter_by(manga_name=m, chapter_number=c, number=p).first().path

    try:
        current_user = User.query.filter_by(username=session['username']).first()
        if current_user:
            bookmark(m, c, p, current_user.id)
    except Exception as e:
        print(e)
    finally:
        return render_template("scans/page.html", m=m, chapters=chapters, pages=pages, c=c, p=p, path=path)
