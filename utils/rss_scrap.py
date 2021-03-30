#!/usr/bin/python

import os, sys
from dotenv import load_dotenv
from feedparser import parse

ROOT_FOLDER = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(ROOT_FOLDER)
load_dotenv(os.path.join(ROOT_FOLDER, ".flaskenv"))
SCAN_FOLDER = os.path.join(os.environ.get("MEDIA_PATH"), "Scans")

from app import app
from app.models import Manga, Chapter
from scrapper import Scrapper
from syncdb import populate_chapter

def main():
    feed = parse("https://www.scan-fr.cc/feed")
    entries = feed.entries
    links = [entry.get("link") for entry in entries]

    with app.app_context():
        for link in links:
            manga_n, chapter_nb = link.split("/")[-2:]
            if Manga.query.filter_by(name = manga_n).first() and not Chapter.query.filter_by(manga_name = manga_n, number = chapter_nb).first():
                manga_p = os.path.join(SCAN_FOLDER, manga_n)
                scp = Scrapper(manga_n, manga_p)
                scp.get_chapter(link)
                populate_chapter(manga_n, chapter_nb, manga_p)

if __name__ == "__main__":
    main()
