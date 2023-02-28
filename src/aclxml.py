import xml.etree.ElementTree as ET
import os
import glob
import pandas as pd


paths = glob.glob("/home/sibava/moonshot/acl-anthology/data/xml/.xml")
papers = []

for path in paths:
    print(path)
    tree = ET.parse(path)
    root = tree.getroot()
    for k in root.iter("year"):
        print(k.text)
        year = k.text
    for k in root.iter("venue"):
        print(k.text)
        venue = k.text
    titles = []
    for k in root.iter("title"):
        if k.text == None:
            print(path)
        title = k.text.lower()
        titles.append(title)
        papers.append([title, venue, year])
    surveys = []
    for title in titles:
        if "survey" in title:
            surveys.append(title)

df = pd.DataFrame(data=papers, columns=["title", "venue", "year"])
print(df.head())
# print(len(surveys))
# print(surveys)
