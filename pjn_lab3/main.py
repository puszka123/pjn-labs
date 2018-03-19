import os
import reader
import re
import time
import operator
from collections import Counter
import pylab as pl
import numpy as np
import dparser
import itertools
import Levenshtein


words = []


def tokenize(data):
    for text in data['items']:
        if not reader.in_2008(text):
            continue
        txt = re.sub(r'<[^>]*>', '', text['textContent'])
        txt = re.sub(r'-\n', '', txt)
        found = re.findall(r'\b[a-zA-ZąęłćżźóńśŚĄĘŁĆŻŹÓŃ]+\b', txt)
        found = [x.lower() for x in found]
        words.extend(found)


def is_word(word):
    if len(word) == 1:
        return False
    return True


def remove(sorted):
    list = []
    for e in sorted:
        if is_word(e[0]):
            list.append(e)
    return list


def levenshtein(ready_list, not_in_dict):
    candidates = []
    for new_word in not_in_dict:
        best_match = None
        dist = 99999
        for candidate in ready_list:
            if candidate[0] == new_word: #the same word
                continue
            new_dist = Levenshtein.distance(candidate[0], new_word)
            if new_dist < dist: #distance
                best_match = candidate
                dist = new_dist
        candidates.append(best_match)
    return candidates



def tests():
    text = 'przedmiot jed-\nnorazowego użytku nr 46 S. Michalskiego. członka zakładu PGP przy ul. Słonecznej 3/54.'
    text = re.sub(r'(-\n)|(\b\w{1,3}\.\s)', '', text)
    found = re.findall(r'\b[a-zA-ZąęłćżźóńśŚĄĘŁĆŻŹÓŃ]+\b', text)
    print(found)
    w = []
    for word in found:
        if is_word(word):
            w.append(word.lower())
    print(w)


def main():
    #tests()
    path_to_json = 'C:/Users/Professional/Desktop/pjn/data/json'
    json_files = [pos_json for pos_json in os.listdir(path_to_json) if pos_json.endswith('.json')]
    for jfile in json_files:
        tokenize(reader.read_json(path_to_json + '/' + jfile))

    frequency_list = Counter(words)
    sorted_list = sorted(frequency_list.items(), key=operator.itemgetter(1), reverse=True)
    ready_list = remove(sorted_list)
    positions = list(range(1, len(ready_list)))
    wds, values = zip(*ready_list)
    pl.hist(values, bins=np.logspace(np.log10(1), np.log10(len(ready_list)), 100))
    pl.gca().set_xscale("log")
    pl.title('positions and number of words occurrences')
    pl.xlabel('position')
    pl.ylabel('occurences')
    pl.show()
    print(len(wds))
    path = 'C:/Users/Professional/Desktop/pjn/polimorfologik-2.1/polimorfologik-2.1.txt'
    dparser.parse_dict(path)
    print(len(dparser.pdict.values()))
    dvals = list(itertools.chain.from_iterable(dparser.pdict.values()))
    not_in_dict = list(set(wds) - set(dvals))
    print(len(not_in_dict))
    chosen_words = []
    for i in range(0, 30):
        chosen_words.append(not_in_dict[i])
    print(chosen_words)
    corrected = levenshtein(ready_list, chosen_words)
    print(corrected)


start_time = time.time()
main()
print("--- %s seconds ---" % (time.time() - start_time))
print(len(words))
