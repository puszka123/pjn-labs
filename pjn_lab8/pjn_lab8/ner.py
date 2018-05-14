user="piotrpuszk@gmail.com"
lpmn="any2txt|wcrft2|liner2({\"model\":\"n82\"})"
import json
import urllib2
import time
url="http://ws.clarin-pl.eu/nlprest2/base"


def upload(text):
    #with open('top/judgment0.json', "rb") as myfile:
    #    doc = myfile.read()
    return urllib2.urlopen(urllib2.Request(url + '/upload/', text.encode('utf-8'), {'Content-Type': 'binary/octet-stream'})).read()


def process(data):
    doc = json.dumps(data)
    taskid = urllib2.urlopen(urllib2.Request(url + '/startTask/', doc, {'Content-Type': 'application/json'})).read()
    time.sleep(0.2)
    resp = urllib2.urlopen(urllib2.Request(url + '/getStatus/' + taskid))
    data = json.load(resp)
    while data["status"] == "QUEUE" or data["status"] == "PROCESSING":
        time.sleep(0.5);
        resp = urllib2.urlopen(urllib2.Request(url + '/getStatus/' + taskid))
        data = json.load(resp)
    if data["status"] == "ERROR":
        print("Error " + data["value"])
        return None
    return data["value"]
