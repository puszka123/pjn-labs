import requests
import json
import os
import re
from word_data import *
from collections import Counter
from loglikelihood import *
import operator

import struct
mysystem = struct.calcsize("P") * 8
print(mysystem)

WORDS = list()
BIGRAMS = list()


def is_letter(char):
    if re.match(r'[a-zA-ZąęłćżźóńśŚĄĘŁĆŻŹÓŃ]', char):
        return True
    else:
        return False


def get_words(line):
    return line.strip().split()


word = 1
count = 0
content = None
with open('data/tagged.txt', 'r', encoding="utf8") as f:
    content = f.readlines()

print(len(content))
for line in content:
    count += 1
    first_char = line[0]
    if is_letter(first_char):
        word = 0
    elif word == 0:
        word = 1
        words = get_words(line)
        found_word = words[0].lower()
        pos = words[1].split(":")[0]
        WORDS.append(Word(found_word, pos))

content = None
prev_word = None
first = True
for word in WORDS:
    if first:
        prev_word = word
        first = False
        continue
    BIGRAMS.append(Bigram(prev_word, word))
    prev_word = word

#for bigram in BIGRAMS:
#    print(bigram)

string_words = [str(x) for x in WORDS]
WORDS = None
count_words = Counter(string_words)
string_words = None
string_bigrams = [str(x) for x in BIGRAMS]
BIGRAMS = None
count_bigrams = Counter(string_bigrams)
string_bigrams = None

d = {}
all_events = sum(count_bigrams.values())
print("calculating ratio")
for bigram in count_bigrams.keys():
    w1, w2 = bigram.split(' ')
    k11 = count_bigrams[bigram]
    k12 = count_words[w2] - k11
    k21 = count_words[w1] - k11
    k22 = all_events - k11 - k12 - k21
    d[bigram] = loglikelihoodRatio(k11=k11, k12=k12, k21=k21, k22=k22)

sorted_d = sorted(d.items(), key=operator.itemgetter(1), reverse=True)

print("printing the result")
result_count = 30
for tuple in sorted_d:
    w1, w2 = tuple[0].split(' ')
    pos1 = w1.split(":")[1]
    pos2 = w2.split(":")[1]
    if pos1 == 'subst' and (pos2 == 'subst' or pos2 == 'adj'):
        print(tuple)
        result_count -= 1
        if result_count <= 0:
            break
