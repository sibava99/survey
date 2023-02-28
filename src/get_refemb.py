import json
import re
from tqdm import tqdm
from time import sleep
import requests
import pandas as pd

SLEEP_SECONDS = 0.011

offset = 0
limit = 1
headers = {"x-api-key": "5NNyAuuUBm4VAUZiEQOL85IeBVtNf9p3tpEPleoe"}
responces = []

code_regex = re.compile(
    "[!\"#$%&'\\\\()*+,-./:;<=>?@[\\]^_`{|}~「」〔〕“”〈〉『』【】＆＊・（）＄＃＠。、？！｀＋￥％]"
)

is_referenced = pd.read_json(
    "/home/sibava/moonshot/selected_survey.jsonl", orient="records", lines=True
)
venue_dict = {
    "International Conference on Computational Linguistics": "COLING",
    "International Conference on Computational Linguistics": "CL",
    "International Conference on Language Resources and Evaluation": "LREC",
    "Annual Meeting of the Association for Computational Linguistics": "ACL",
    "Computational Linguistics": "CL",
    "Conference on Empirical Methods in Natural Language Processing": "EMNLP",
    "North American Chapter of the Association for Computational Linguistics": "NAACL",
    "International Journal of Computational Linguistics and Chinese Language Processing": "IJCNLP",
    "Transactions of the Association for Computational Linguistics": "TACL",
}
pd.set_option("display.max_rows", 100)
pd.set_option("display.max_colwidth", 80)
is_referenced["venue"] = is_referenced["venue"].replace(venue_dict)
is_referenced["venue"].value_counts()
target_venue = ["LREC", "CL", "ACL", "EMNLP", "NAACL", "COLING", "AACL", "TACL"]
selected = is_referenced[is_referenced["venue"].isin(target_venue)]
references = selected["references"].explode()
reference_ids = [x["paperId"] for x in references.to_list() if not x["paperId"] == None]
reference_ids = list(set(reference_ids))
print(len(reference_ids))

reference_embs = []
for paperId in tqdm(reference_ids):
    responce = requests.get(
        f"http://api.semanticscholar.org/graph/v1/paper/{paperId}?fields=title,year,citationCount,embedding",
        headers=headers,
    )
    txt = responce.text
    d = json.loads(txt)
    reference_embs.append(d)

df = pd.DataFrame(reference_embs)

df.to_json(
    "/home/sibava/moonshot/ref_embs.jsonl",
    orient="records",
    lines=True,
    force_ascii=False,
)
