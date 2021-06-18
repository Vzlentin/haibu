#!/usr/bin/python

import os, sys, re

ROOT_FOLDER = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(ROOT_FOLDER)

from extensions import db
from config import MEDIA_PATH

from app.models import *
from app import app

def clean_non_numeric(string):
    return re.sub("[^0-9]", "", string)

def populate_scans(path):

    print(" - Populating database with scans")

    for manga_name in sorted(os.listdir(path)):

        try: 

            print(f" - Populating {manga_name}")

            if not Manga.query.filter_by(name=manga_name).first():
                m = Manga(name=manga_name)
                db.session.add(m)
                db.session.commit()

            manga_path = os.path.join(path, manga_name)

            for chapter_number in sorted(os.listdir(manga_path), key=lambda i: float(clean_non_numeric(i))):

                try:
                    populate_chapter(manga_name, chapter_number, manga_path)
                except:
                    raise RuntimeError(f"Error populating {manga_name} {chapter_number}")
        except:
            raise


def populate_chapter(manga_name, chapter_number, manga_path):

    m = Manga.query.filter_by(name=manga_name).first()

    if not Chapter.query.filter_by(number=chapter_number, manga_id=m.id, manga_name=m.name).first():

        print(chapter_number)

        c = Chapter(number=chapter_number, manga_id=m.id, manga_name=m.name)
        db.session.add(c)
        db.session.commit()
        chapter_path = os.path.join(manga_path, chapter_number)

        for page_filename in sorted(os.listdir(chapter_path), key=lambda i: int(clean_non_numeric(os.path.splitext(i)[0]))):

            page_path = os.path.join(manga_name, (os.path.join(chapter_number, page_filename)))
            page_number = os.path.splitext(page_filename)[0]
            p = Page(number=page_number, manga_id=m.id, manga_name=m.name, chapter_id=c.id, chapter_number=c.number, path=page_path)
            db.session.add(p)
            db.session.commit()


def populate_anime(path):

    print(" - Populating database with animes")

    for anime_name in sorted(os.listdir(path)):
        if not Anime.query.filter_by(name=anime_name).first():
            a = Anime(name=anime_name)
            db.session.add(a)
            db.session.commit()
            anime_path = os.path.join(path, anime_name)

            for season_name in sorted(os.listdir(anime_path)):
                s = Season(name=season_name, anime_id=a.id, anime_name=a.name)
                db.session.add(s)
                db.session.commit()
                season_path = os.path.join(anime_path, season_name)

                for episode_filename in sorted(os.listdir(season_path)):
                    episode_path = os.path.join(anime_name, (os.path.join(season_name, episode_filename)))
                    episode_name = os.path.splitext(episode_filename)[0]
                    e = Episode(name=episode_name, anime_id=a.id, anime_name=a.name, season_id=s.id, season_name=s.name, path=episode_path)
                    db.session.add(e)
                    db.session.commit()

def genesis():
    if not User.query.filter_by(username='vzl3ntin').first():

        print(" - Creating user 001")

        u = User(username='vzl3ntin')
        db.session.add(u)
        db.session.commit()

def main(scans_static_path, anime_static_path):

    print(" - Populating db")

    db.init_app(app)
    with app.app_context():
        if not os.path.exists("app.db"):
            db.create_all()

        genesis()

        populate_scans(scans_static_path)

        populate_anime(anime_static_path)

if __name__ == "__main__":
    app_folder = os.path.join(ROOT_FOLDER, "app")
    scans_static_path = os.path.join(app_folder, "scans/static")
    anime_static_path = os.path.join(app_folder, "anime/static")
    main(scans_static_path, anime_static_path)
