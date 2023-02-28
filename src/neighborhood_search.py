import json
from tqdm import tqdm
import argparse
import numpy as np
import pandas as pd
from math import dist


def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--surveys", help="surveys jsonl path")
    parser.add_argument("-r", "--references", help="references jsonl path")
    return parser


def main():
    parser = create_parser()
    args = parser.parse_args()

    pd.set_option("display.max_colwidth", 80)
    surveys = pd.read_json(args.surveys, orient="recores", lines=True)
    references = pd.read_json(args.references, orient="recores", lines=True)

    reference_ids = references["paperId"].to_list()
    g = 0
    tp = 0
    macro = 0
    f1 = 0
    for i, row in surveys.iterrows():
        survey_emb = row["embedding"]["vector"]
        references["distance"] = (
            references["embedding"]
            .map(lambda x: x["vector"])
            .map(lambda x: dist(x, survey_emb))
        )
        # print(row["title"])
        # print(references.sort_values("distance").head(5)["title"])
        preds = references.sort_values("distance").head(20)["paperId"].to_list()
        golds = [x["paperId"] for x in row["references"] if not x["paperId"] == None]
        # golds = set(golds) & set(reference_ids)
        # print(set(golds) - set(reference_ids))

        g += len(golds)
        tp += len(set(preds) & set(golds))
        if g != 0:
            macro += tp / g
            f1 += g / 20
        else:
            macro += 1
        print(f"{len(set(preds) & set(golds))}/{len(golds)}")
    print(f"{tp}/{g}")
    print(f"macro recall {macro/len(surveys)}")
    print(f"f1 recall {f1/len(surveys)}")
    # print(f"{tp}/{len(surveys)*5}")


if __name__ == "__main__":
    main()
