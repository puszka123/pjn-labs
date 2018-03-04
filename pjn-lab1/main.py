# coding=utf-8
import re
import os
import reader
import time
import matplotlib.pyplot as plt

money = []


def normalized(value, zeros):
    return float(value) * zeros


def parse_value(matched):
    value = re.sub(r'[\s]+', '', matched[0], re.UNICODE)
    # grosze
    index = value.rfind(',')
    index2 = value.rfind('.')
    if index < index2:
        index = index2
    gindex = len(value) - 3  # 12.312,98 (pozycja , lub . oddzielajacego grosze)

    if not index == -1:
        value = re.sub(r'[\.,]', '', value[:index]) + value[index:]
        value = re.sub(r'[\.,]', '.', value)

    if index == gindex:  # z groszami
        return float(value)

    matched = list(map(str.strip, matched))
    if 'tys' in matched:
        return normalized(value, 1000)
    elif 'mln' in matched:
        return normalized(value, 1000000)
    elif 'mld' in matched:
        return normalized(value, 1000000000)
    else:
        value = re.sub(r'[\.,]', '', value, re.UNICODE)
        return float(value)


def find_values(data):
    for text in data['items']:
        if not reader.in_2008(text):
            continue
        # liczba taka jak '1203120' lub '123,1541.123,11321' lub '123 2100 3210 3210'
        # jednostka 'mld' | 'mln' | 'tys' lub kwota slownie '(kwota slownie)' lub stare w postaci: '(starych|stare) lub 'starych|stare' wystepujace max 3 razy
        # zlotych lub zlote na samym koncu
        found = re.findall(r'((\b\d+[\d,]*\b)|(\b\d+\s?[\d.]*,?\d{2}?\b)|(\b\d+[\d\s]+,?\d{2}?\b))\s?'
                           r'((\bmld\b\s?)|(\bmln\b\s?)|(\btys\b\s?)|(\b\(?star\w{1,3}\)?\b\s?)|(\([\w\s]+\)\s?)){0,3}'
                           r'((\bzłot\w{1,3}\b)|(\bzł\.?\b))', text['textContent'])
        for matched in found:
            value = parse_value(matched)
            money.append(value)


def main():
    path_to_json = 'C:/Users/Professional/Desktop/pjn/data/json'
    json_files = [pos_json for pos_json in os.listdir(path_to_json) if pos_json.endswith('.json')]
    for jfile in json_files:
        find_values(reader.read_json(path_to_json + '/' + jfile))


start_time = time.time()
main()
print("--- %s seconds ---" % (time.time() - start_time))
print(len(money))
print(money)
money__over_m = [i for i in money if i >= 1000000]
money_below_m = [i for i in money if i < 1000000]
print(len(money__over_m))
print(len(money_below_m))
print(money__over_m)
print(max(money))
print(min(money__over_m))
plt.hist(money, bins='doane')
plt.title('Wartosci wystepujace w orzeczeniach w roku 2008')
plt.xlabel('Wartosc pieniezna')
plt.ylabel('Czestosc')
plt.show()

plt.hist(money__over_m, bins='doane')
plt.title('Wartosci powyzej miliona wystepujace w orzeczeniach w roku 2008')
plt.xlabel('Wartosc pieniezna')
plt.ylabel('Czestosc')
plt.show()

plt.hist(money_below_m, bins='doane')
plt.title('Wartosci ponizej miliona wystepujace w orzeczeniach w roku 2008')
plt.xlabel('Wartosc pieniezna')
plt.ylabel('Czestosc')
plt.show()
