import json


def read_json(path):
    data = json.load(open(path))
    return data
