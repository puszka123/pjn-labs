import requests
import os
import reader


url = 'http://localhost:9200'
count = 0


def tag_judgment(data):
    global count
    for text in data['items']:
        if not reader.in_2008(text):
            continue
        count += 1
        response = requests.post(url, text['textContent'].encode('utf-8'))
        with open('tagged.txt', 'a') as f:
            f.writelines(response.text)


path_to_json = 'judgments'
json_files = [pos_json for pos_json in os.listdir(path_to_json) if pos_json.endswith('.json')]
for jfile in json_files:
    tag_judgment(reader.read_json(path_to_json + '/' + jfile))

print(count)
