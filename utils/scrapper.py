#!/usr/bin/python

from bs4 import BeautifulSoup
import requests, os

class Scrapper:

    def __init__(self, mname, dest):
        self._baseurl = "https://www.scan-fr.cc/manga"
        self._mname = mname
        self._dest = dest
        if not os.path.exists(dest):
            os.mkdir(dest)

    def get_all_chapters(self):
        chapter_links = Scrapper._get_chapter_links(os.path.join(self._baseurl, self._mname))
        for chap_link in reversed(chapter_links):
            self.get_chapter(chap_link)

    def get_chapter(self, chapter_link):

        print(f"Downloading {chapter_link}...")
        chapter_path = os.path.join(self._dest, chapter_link.split("/")[-1])

        if not os.path.exists(chapter_path):
            os.mkdir(chapter_path)

            page_links = Scrapper._get_page_links(chapter_link)
            for page_link in page_links:
                image_path = os.path.join(chapter_path, page_link.split("/")[-1])
                
                if not os.path.exists(image_path):
                    Scrapper._download_image(page_link, image_path)

    @staticmethod
    def _get_chapter_links(url):
        r =  requests.get(url)
        soup = BeautifulSoup(r.content, features="lxml")
        return [a["href"] for a in soup.find_all("a", href=True) if url in a["href"]]

    @staticmethod
    def _get_page_links(url):
        r =  requests.get(url)
        soup = BeautifulSoup(r.content, features="lxml")
        return [img["data-src"].strip() for img in soup.find_all("img", {"data-src": True})]

    @staticmethod
    def _download_image(url, path):
        r = requests.get(url)
        with open(path, 'wb') as f:
            f.write(r.content)
