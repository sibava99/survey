import requests
import json
from tqdm import tqdm
from pprint import pprint

offset = 0
limit = 100
keywords = ["NAACL", "survey"]
query = "+".join(keywords)
print(query)
responce = requests.get(
    f"http://api.semanticscholar.org/graph/v1/paper/search?query={query}&offset={offset}&limit={limit}&fields=title,venue,fieldsOfStudy"
)
txt = responce.text
d = json.loads(txt)
pprint(d)

data = d["data"]

data = [
    x
    for x in data
    if (
        x["venue"] != None
        and x["fieldsOfStudy"] != None
        and x["venue"] == "NAACL"
        and "Computer Science" == x["fieldsOfStudy"][0]
    )
]
data_new = []
for p in tqdm(data):
    print("\n")
    print(p["title"])
    val = ""
    while not (val == "i" or val == "o"):
        val = input()
    if val == "i":
        data_new.append(p)
    elif val == "o":
        continue
    else:
        continue

d["data"] = data_new

with open("out.txt", mode="a") as f:
    json.dump(d, f)
