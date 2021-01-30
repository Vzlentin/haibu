#!/usr/bin/python

import pandas as pd
import os

df = pd.DataFrame()
os.chdir("/home/vzl3ntin/Documents/Anime")
works = os.listdir()

workk, seasonn, episodee, pathh = [], [], [], []

for work in works:
  work_path = os.path.join(os.getcwd(), work)
  seasons = os.listdir(work_path)

  for season in seasons:
    season_path = os.path.join(work_path, season)
    episodes = os.listdir(season_path)

    for episode in episodes:
      path = os.path.relpath(os.path.join(season_path, episode))
      info = path.split('/')

      pathh.append(path)
      workk.append(info[0])
      seasonn.append(info[1])
      episodee.append(info[2])

df["path"] = pathh
df["work"] = workk
df["season"] = seasonn
df["episode"] = episodee

df = df.sort_values(by=["season", "work","episode"]).reset_index(drop=True)
df.to_csv(os.path.join(os.path.dirname(os.path.realpath(__file__)), "data/anime.csv"), index=False)
