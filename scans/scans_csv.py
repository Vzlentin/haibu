#!/usr/bin/python

import pandas as pd
import os

df = pd.DataFrame()
os.chdir("/home/vzl3ntin/Documents/Scans")
works = os.listdir()

workk, chapp, pagee, pathh = [], [], [], []

for work in works:
  work_path = os.path.join(os.getcwd(), work)
  chapters = os.listdir(work_path)

  for chapter in chapters:
    chapter_path = os.path.join(work_path, chapter)
    pages = os.listdir(chapter_path)

    for page in pages:
      path = os.path.relpath(os.path.join(chapter_path, page))
      info = path.split('/')

      pathh.append(path)
      workk.append(info[0])
      chapp.append(info[1])
      pagee.append(info[2])

df["path"] = pathh
df["work"] = workk
df["chap"] = chapp
df["page"] = pagee

def without_last_4chars(x):
    return(int(x[:-4]))

df.page = df.page.apply(without_last_4chars)
df = df.sort_values(by=["chap", "work","page"]).reset_index(drop=True)
df.to_csv(os.path.join(os.path.dirname(os.path.realpath(__file__)), "data/scans.csv"), index=False)
