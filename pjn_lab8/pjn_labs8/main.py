from xmlreader import *
from collections import Counter
import re
import numpy as np
import matplotlib.pyplot as plt
from expression import Expression
import operator

all = []
detailed = []


def get_expressions_from_sentence(sentence):
    expressions = []
    tokens = get_elements_by_name(sentence, 'tok')
    for token in tokens:
        token_name = get_elements_by_name(token, 'orth')
        #print(token_name[0].childNodes[0].nodeValue)
        anns = get_elements_by_name(token, 'ann')
        for a in anns:
            #print(a.attributes['chan'].value + ' ' + a.childNodes[0].nodeValue)
            index = int(a.childNodes[0].nodeValue)
            if not index == 0:
                added = False
                for expression in expressions:
                    if expression.class_index == index and expression.class_name == a.attributes['chan'].value:
                        expression.tokens.append(token_name[0].childNodes[0].nodeValue)
                        added = True
                        break
                if not added:
                    expressions.append(Expression(token_name[0].childNodes[0].nodeValue, a.attributes['chan'].value, index))
    return expressions


def get_all():
    global all
    found = False
    for i in range(100):
        xmldoc = get_xml_doc('out/judgment' + str(i) + ".ccl")
        itemlist = get_elements_by_name(xmldoc, 'sentence')
        for sentence in itemlist:
            expressions = get_expressions_from_sentence(sentence)
            all.extend(expressions)


def main():
    get_all()
    general = []
    exact = []
    for expression in all:
        exact.append(expression.class_name)
        general.append(expression.general_class_name)
    f1 = Counter(exact)
    f2 = Counter(general)
    print(f1)
    plt.bar(f1.keys(), f1.values(), color='g')
    plt.show()
    plt.bar(f2.keys(), f2.values(), color='g')
    plt.show()
    top_expressions1 = {}
    for expression in all:
        key = (expression.class_name, expression.get_tokens())
        if key in top_expressions1:
            top_expressions1[key] += 1
        else:
            top_expressions1[key] = 1
    print(top_expressions1)
    top = sorted(top_expressions1.items(), key=operator.itemgetter(1), reverse=True)
    for i in range(100):
        print(top[i])
    print('-----------------------------------------------------------------')
    general_top = {}
    for expression in all:
        key = expression.general_class_name
        if key in general_top:
            general_top[key].append(expression.get_tokens())
        else:
            general_top[key] = [expression.get_tokens()]
    for key in general_top.keys():
        freq = Counter(general_top[key])
        sorted_general = sorted(freq.items(), key=operator.itemgetter(1), reverse=True)
        print(key)
        for i in range(10):
            if i < len(sorted_general):
                print(sorted_general[i])
        print('-----------------------------------------------------------------')
main()
