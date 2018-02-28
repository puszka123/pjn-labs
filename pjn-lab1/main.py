# coding=utf-8
import re
import os
import reader


def match_values(data):
    for text in data['items']:
        #zakladam ze wartosc pieniezna jest postaci: <liczba> <jednostka>|starych|stare|<(kwota slownie)> zlotych|zlote np. 270 (dwiescie siedemdziesiat) starych zlotych
        #mozna wylapac niepoprawna liczbe np. 270.....2321312..3243.
        #liczba taka jak '1203120' lub '123,1541.123,11321' lub '123 2100 3210 3210'
        #jednostka 'mld' | 'mln' | 'tys' lub kwota slownie '(kwota slownie)' lub stare w postaci: '(starych|stare) lub 'starych|stare' wystepujace max 3 razy
        #zlotych lub zlote na samym koncu
        found = re.findall(ur'((\d+)|(\d[,\.\d]+)|(\d[\d\s]+))\s?'
                           ur'((\bmld\.?\b\s?)|(\bmln\.?\b\s?)|(\btys\.?\b\s?)|(\b\(?star\w{1,3}\)?\b\s?)|(\([\w\s]+\)\s?)){0,3}'
                           ur'((\bzłot\w{1,3}\b)|(\bzł\.?\b))', text['textContent'], re.UNICODE)
        for matched in found:
            if matched[4]:
                print matched[0] + ' ' + matched[4] + ' ' + matched[10]
            #else:
             #   print matched[0] + ' ' + matched[10]



def main():
    path_to_json = 'C:/Users/Professional/Desktop/pjn/data/json'
    json_files = [pos_json for pos_json in os.listdir(path_to_json) if pos_json.endswith('.json')]
    for file in json_files:
        match_values(reader.read_json(path_to_json+'/'+file))



main()
