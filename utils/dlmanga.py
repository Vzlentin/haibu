#!/usr/bin/python

import os, sys
from dotenv import load_dotenv

ROOT_FOLDER = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(ROOT_FOLDER)
load_dotenv(os.path.join(ROOT_FOLDER, ".flaskenv"))
SCAN_FOLDER = os.path.join(os.environ.get("MEDIA_PATH"), "Scans")

from scrapper import Scrapper
import requests


if __name__ == "__main__":

    if len(sys.argv) > 1:
        manga_name = sys.argv[1]
        try:

            requests.get(f"https://www.scan-fr.cc/manga/{manga_name}").raise_for_status()
            destination = os.path.join(SCAN_FOLDER, manga_name)
            scp = Scrapper(manga_name, destination)
            scp.get_all_chapters()

        except requests.exceptions.HTTPError:
            print("Bad manga name")
            raise