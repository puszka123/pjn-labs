from elasticsearch import Elasticsearch
from datetime import datetime
from dateutil.parser import parse
import os
import reader
import matplotlib.pyplot as plt

es = Elasticsearch([{'host': 'localhost', 'port': 9200}])


index_body = {
        'settings': {
            'analysis': {
                'analyzer': {
                    'my_analyzer': {
                        'type': 'custom',
                        'tokenizer': 'standard',
                        'filter': ['morfologik_stem', 'lowercase']
                    }
                }
            }
        },
        'mappings': {
            'judgment': {
                'properties': {
                    'text': {'type': 'text', 'analyzer': 'my_analyzer'},
                    'judgmentDate': {'type': 'date'},
                    'caseNumber': {'type': 'keyword', },
                    'judges.name': {'type': 'keyword'}
                }
            }
        }
}


szkoda_query = {
    "query": {
        "match": {
            "text": "szkoda"
        }
    }
}

test = {
    'text': 'trwałego woda woda uszczerbku na woda zdrowiu',
    'judgementDate': datetime.now(),
    'caseNumber': 'U 32/08',
    'judges.name': ['Grzegorz Piączętkowiłski']
}

phrase_query = {
    "query": {
        "match_phrase": {
            "text": "trwały uszczerbek na zdrowie"
        }
    }
}

special_phrase_query ={
    "query": {
        "span_near" : {
            "clauses" : [
                {"span_term": {"text" : "trwały"}},
                {"span_term": {"text" : "uszczerbek"}},
                {"span_term": {"text" : "na"}},
                {"span_term": {"text" : "zdrowie"}}
            ],
            "slop": 2,
            "in_order": True
        }
    }
}

judges_aggs = {
        "size": 0,
        "aggs": {
            "group_by_judge": {
              "terms": {
                "field": "judges.name"
              }
            }
        }
}

month_aggs = {
        "aggs": {
            "docs_per_month": {
                "date_histogram": {
                    "field": "judgmentDate",
                    "interval": "month"
                }
            }
        }
}

all_query = {
        "query": {
            "match_all": {}
        }
}


id = 0
def save_in_es(data):
    global id
    for text in data['items']:
        if not reader.in_2008(text):
            continue

        judges = []
        for judge in text['judges']:
            judges.append(judge['name'])
        judgment_doc = {
            'text': text['textContent'],
            'judgmentDate': parse(text['judgmentDate']),
            'caseNumber': text['courtCases'][0]['caseNumber'],
            'judges.name': judges
        }
        print(judges)
        res = es.index(index='lab', doc_type='judgment', body=judgment_doc, id=id)
        print(res)
        id += 1


def init_es():
    # creating the index
    es.indices.delete(index='lab', ignore=[400, 404])
    res = es.indices.create(index='lab', body=index_body, ignore=400)
    print(res)

    path_to_json = 'C:/Users/Professional/Desktop/pjn/data/json'
    json_files = [pos_json for pos_json in os.listdir(path_to_json) if pos_json.endswith('.json')]
    for jfile in json_files:
        save_in_es(reader.read_json(path_to_json + '/' + jfile))


def testing():
    #es.indices.delete(index='lb1', ignore=[400, 404])
    res = es.indices.create(index='lb1', body=index_body, ignore=400)
    print(res)
    res = es.index(index='lb1', doc_type='judgment', body=test, id=4)
    print(res)
    res = es.search(index='lb1', doc_type='judgment', body=all_query)
    print(res['hits']['total'])  # should be 4352
    res = es.search(index='lb1', doc_type='judgment', body=special_phrase_query)
    print(res['hits']['total'])
    res = es.search(index='lb1', doc_type='judgment', body=judges_aggs)
    for bucket in res['aggregations']['group_by_judge']['buckets']:
        print(bucket['key'] + ' ' + str(bucket['doc_count']))


def main():
    #init_es()
    #testing()
    res = es.search(index='lab', doc_type='judgment', body=all_query)
    print(res['hits']['total']) #should be 4352
    res = es.search(index='lab', doc_type='judgment', body=szkoda_query)
    print(res['hits']['total'])
    res = es.search(index='lab', doc_type='judgment', body=phrase_query)
    print(res['hits']['total'])
    res = es.search(index='lab', doc_type='judgment', body=special_phrase_query)
    print(res['hits']['total'])
    res = es.search(index='lab', doc_type='judgment', body=judges_aggs)
    top = 3
    for i in range(0, 3):
        print(res['aggregations']['group_by_judge']['buckets'][i])
    res = es.search(index='lab', doc_type='judgment', body=month_aggs)

    d = {}
    month = 0
    for i in res['aggregations']['docs_per_month']['buckets']:
        print(i)
        d[month] = i['doc_count']
        month += 1
    plt.bar(d.keys(), d.values(), 1, color='b')
    plt.title('Number of cases per month')
    plt.xlabel('Months')
    plt.ylabel('number of cases')
    plt.show()


main()
