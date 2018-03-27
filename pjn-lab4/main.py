import os
import reader
import re
import time
from collections import Counter
import operator
import math
from collections import OrderedDict
import numpy as np


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


def get_special_list():
    bigrams = []
    for i in range(0, len(words)-1):
        bigrams.append(words[i] + ' ' + words[i+1])
    return Counter(bigrams)


def pmi(word1, word2, unigram_freq, bigram_freq, unigram_sum, bigram_sum):
    prob_word1 = unigram_freq[word1] / unigram_sum
    prob_word2 = unigram_freq[word2] / unigram_sum
    prob_word1_word2 = bigram_freq[" ".join([word1, word2])] / bigram_sum
    return math.log(prob_word1_word2/float(prob_word1*prob_word2), 2)


def calculate_pmi(unigrams, bigrams):
    d = {}
    unigram_sum = float(sum(unigrams.values()))
    bigram_sum = float(sum(bigrams.values()))
    for bigram in bigrams.keys():
        word1, word2 = bigram.split(' ')
        bigram_pmi = pmi(word1, word2, unigrams, bigrams, unigram_sum, bigram_sum)
        d[bigram] = bigram_pmi
    return d


def H(k):
    N = np.sum(k)
    return np.sum((k/N)*np.log(k/N + (k == 0)))


def llr(k):
    return 2*np.sum(k)*(H(k) - H(k.sum(axis=1) - H(k.sum(axis=0))))


def calculate_llr(bigrams, unigrams, bigrams_sum):
    d = {}
    k = np.array([[0, 0], [0, 0]])
    for bigram in bigrams:
        w1, w2 = bigram.split(' ')
        k[0][0] = bigrams[bigram]
        k[0][1] = unigrams[w2] - k[0][0]
        k[1][0] = unigrams[w1] - k[0][0]
        k[1][1] = bigrams_sum - k[0][0] - k[0][1] - k[1][0]
        d[bigram] = llr(k)
    return d


def main():
    global words
    #tests()
    path_to_json = 'judgments'
    json_files = [pos_json for pos_json in os.listdir(path_to_json) if pos_json.endswith('.json')]
    for jfile in json_files:
        tokenize(reader.read_json(path_to_json + '/' + jfile))
    unigrams = Counter(words)
    bigrams = get_special_list()
    words = []
    print(len(bigrams))
    bigrams_pmi = calculate_pmi(unigrams, bigrams)
    bigrams_pmi = OrderedDict(sorted(bigrams_pmi.items(), key=lambda x: x[1], reverse=True))
    count = 0
    for e in bigrams_pmi:
        count += 1
        print(e + ', ', end='')
        if count > 30:
            print('')
            break
    bigrams_llr = calculate_llr(bigrams, unigrams, sum(bigrams.values()))
    bigrams_llr = OrderedDict(sorted(bigrams_llr.items(), key=lambda x: x[1], reverse=True))
    count = 0
    for e in bigrams_llr:
        count += 1
        if count == 1:
            print(e + ' ' + str(bigrams_llr[e]))
        print(e + ', ', end='')
        if count > 30:
            print('')
            break


start_time = time.time()
main()
print("--- %s seconds ---" % (time.time() - start_time))
print(len(words))
