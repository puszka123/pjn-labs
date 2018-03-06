import re
import os
import reader
import time

szkoda_ends = ['a', 'y', 'zie', 'ę', 'ą', 'o', 'om', 'ami', 'ach']
words = []

def proper(word):
    if word.lower() == 'szkód':
            return True
    elif word[5:] in szkoda_ends:
        return True
    return False

def find_szkoda(data):
    for text in data['items']:
        if not reader.in_2008(text):
            continue
        found = re.findall(r'\b[Ss]zk[oó]d\w{0,3}\b', text['textContent'])

        for word in found:
            if proper(word):
                words.append(word)
                break


def main():
    path_to_json = 'C:/Users/Professional/Desktop/pjn/data/json'
    json_files = [pos_json for pos_json in os.listdir(path_to_json) if pos_json.endswith('.json')]
    for jfile in json_files:
        find_szkoda(reader.read_json(path_to_json + '/' + jfile))


start_time = time.time()
main()
print("--- %s seconds ---" % (time.time() - start_time))
print(len(words))
print(words)
