import re
import numpy as np

pdict = {}


def parse_dict(fname):
    with open(fname, encoding="utf8") as f:
        content = f.readlines()
    for e in content:
        words = re.findall(r'\w+', e)
        words[0] = words[0].lower()
        words[1] = words[1].lower()
        if words[0] in pdict.keys():
            pdict[words[0]].append(words[1])
        else:
            pdict[words[0]] = [words[1], ]
