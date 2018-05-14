import json
import re
import io


def in_2008(text):
    date = text['judgmentDate']
    date = re.split(r'[-.\\/]', date)
    if '2008' in date:
        return True
    else:
        return False


def read_json(path):
    with io.open(path, encoding='utf-8') as fh:
        data = json.load(fh)
    return data


def write_json(path, data):
    with open(path, 'w') as outfile:
        json.dump(data, outfile)
