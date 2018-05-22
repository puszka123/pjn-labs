import json
import re
from gensim.models import Word2Vec
from gensim.models.phrases import Phraser, Phrases

judgments = list()
sentencesAll = list()
trigramSentences = list()
model = []
judgmentsText = ''

htmlTags = r'<[^>]*>'

newline = r'-\n'


def read_file(fileName):
    global judgments
    data = json.load(open(fileName, encoding="utf8"))
    judgments.extend(data['items'])


def filter_html_tags():
    global judgments, judgmentsText, newline, htmlTags
    print("filter_html_tags")
    length = len(judgments)
    temp_judgments_list = list()
    for index in range(length):
        judgment = judgments.pop()
        temp = re.sub(htmlTags, "", judgment['textContent'])
        temp = re.sub(newline, "", temp)
        temp_judgments_list.append(temp)
        judgmentsText = ''.join(temp_judgments_list)
    del judgments[:]


def detect_phrases():
    global  sentencesAll, trigramSentences
    print("detect_phrases")
    sentences = judgmentsText.split('.')
    for sentence in sentences:
        sentencesAll.append(sentence.strip().split())
    phrases = Phrases(sentencesAll)
    bigram = Phraser(phrases)
    trigram = Phrases(bigram[sentencesAll])
    for sent in sentencesAll:
        trigramSentences.append(trigram[bigram[sent]])


def train():
    global model, trigramSentences
    print("train")
    model = Word2Vec(trigramSentences, sg=0, window=5, size=300, min_count=3)
    print(model)
    model.save('./model/word2vec_model')


def load_model():
    global model
    model = Word2Vec.load('./model/word2vec_model')


judgmentNr = 100
while judgmentNr < 560:
    judgments = list()
    judgmentsText = ''
    sentencesAll = list()
    print("read_file")
    for i in range(judgmentNr, judgmentNr+10):
        fileName = './judgments/judgments-' + str(i) + '.json'
        read_file(fileName)
    filter_html_tags()
    detect_phrases()
    judgmentNr += 10

judgments = list()
judgmentsText = ''
sentencesAll = list()
train()
load_model()
word7 = ["Sąd_Najwyższy", "Trybunał_Konstytucyjny", "kodeks_cywilny", "kpk", "sąd_rejonowy", "szkoda", "wypadek", "kolizja", "nieszczęście", "rozwód"]
for word in word7:
    print(word)
    print(model.most_similar(word, topn=3))

print(model.most_similar(positive=['Sąd_Najwyższy', 'konstytucja'], negative=['kpc'], topn=5))
print(model.most_similar(positive=['pasażer', 'kobieta'], negative=['mężczyzna'], topn=5))
print(model.most_similar(positive=['samochód', 'rzeka'], negative=['droga'], topn=5))
