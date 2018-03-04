import json
import re

def in_2008(text):
    date = text['judgmentDate']
    date = re.split(r'[-.\\/]', date)
    if '2008' in date:
        return True
    else:
        return False

def read_json(path):
    data = json.load(open(path, encoding="utf8"))
    return data
