#-*- coding: utf-8 -*-
import reader
import os
import urllib2
from datetime import datetime
from ner import process, upload, lpmn, url, user


all_jugdments = []
top_judgments = []


def sort_by_date():
    return sorted(all_jugdments, key=lambda x: datetime.strptime(x['judgmentDate'], '%Y-%m-%d'))


def load_judgments(data):
    for jsondoc in data['items']:
        if not reader.in_2008(jsondoc):
            continue
        all_jugdments.append(jsondoc)


def process_top_judgments():
    global top_judgments
    for i in range(100):
        simple_text = top_judgments[i]['textContent']
        fileid = upload(simple_text)
        print("Processing: " + str(fileid))
        data = {'lpmn': lpmn, 'user': user, 'file': fileid}
        data = process(data)
        if data is None:
            return
        data = data[0]["fileID"]
        content = urllib2.urlopen(urllib2.Request(url + '/download' + data)).read()
        with open('out/' + os.path.basename('judgment'+str(i)) + '.ccl', "w") as outfile:
            outfile.write(content)


def main():
    global top_judgments
    #load jsons to global all_judgments
    path_to_json = 'judgments'
    json_files = [pos_json for pos_json in os.listdir(path_to_json) if pos_json.endswith('.json')]
    for jfile in json_files:
        load_judgments(reader.read_json(path_to_json + '/' + jfile))
    #sort by date
    sort_by_date()
    #save
    #for i in range(100):
    #    reader.write_json('top/judgment'+str(i)+'.json', all_jugdments[i])
    top_judgments = all_jugdments[:100]
    process_top_judgments()


main()
