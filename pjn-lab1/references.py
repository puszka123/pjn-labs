import re
import os
import reader
import time
import matplotlib.pyplot as plt

f = []

def find_references(data):
    for item in data['items']:
        if not reader.in_2008(item):
            continue
        for reference in item['referencedRegulations']:
            found = re.findall(r'(\bUstawa\b\s+\bz\b\s+\bdnia\b\s+\b23\b\s+\bkwietnia\b\s+\b1964\b\s+r\.\s+-\s+\bKodeks\b\s+\bcywilny\b)'
                               r'[\S\s]+(\bart.\s+\b445\b)', reference['text'])
            f.extend(found)


def main():
    path_to_json = 'C:/Users/Professional/Desktop/pjn/data/json'
    json_files = [pos_json for pos_json in os.listdir(path_to_json) if pos_json.endswith('.json')]
    for jfile in json_files:
        find_references(reader.read_json(path_to_json + '/' + jfile))


start_time = time.time()
main()
print("--- %s seconds ---" % (time.time() - start_time))
print(f)
print(len(f))
