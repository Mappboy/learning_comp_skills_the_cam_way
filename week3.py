"""
Cricket Game
# TODO
# https://en.wikipedia.org/wiki/List_of_nicknames_used_in_cricket
"""

import pprint

import pandas as pd
import requests
from bs4 import BeautifulSoup

resp = requests.get(
    "https://en.wikipedia.org/wiki/List_of_Australia_Test_cricketers"
)
pprint.pprint(resp.content)

soup = BeautifulSoup(resp.content, 'lxml')
table = soup.find_all('table')[0]
df = pd.read_html(str(table))
df = df[0]
names = df["Australian Test cricketers"]["Name"]
first_names = [_.split()[0] for _ in names]
last_names = [_.split()[-1] for _ in names]
df.to_csv("cricket_wiki.csv")
