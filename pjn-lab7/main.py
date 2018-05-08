import wnxmlconsole
from node import Node
import graph
import networkx as nx
import pylab as plt
import sys

wn = wnxmlconsole.get_ready_wnquery()

group1 = [("szkoda", 2), ("strata", 1), ("uszczerbek", 1), ("szkoda majątkowa", 1), ("uszczerbek na zdrowiu", 1), ("krzywda", 1), ("niesprawiedliwość", 1), ("nieszczęście", 2)]
group2 = [("wypadek", 1), ("wypadek komunikacyjny", 1), ("kolizja", 2), ("zderzenie", 2), ("kolizja drogowa", 1), ("katastrofa budowlana", 1), ("wypadek drogowy", 1)]


def get_s_m(group):
    result = []
    for i in range(0, len(group)-1):
        isSynonym = False
        isHyponym = False
        for j in range(i + 1, len(group)):
            print(group[i][0] + " and " + group[j][0])
            synset1 = wn.lookUpSense(group[i][0], group[i][1], "n")
            synset2 = wn.lookUpSense(group[j][0], group[j][1], "n")
            # bliskoznaczność
            try:
                foundtarg = wn.isIDConnectedWith(synset1.wnid, "n", "bliskoznaczność", synset2.wnid)
                if foundtarg:
                    result.append((group[i][0], group[j][0], "bliskoznaczność"))
                    continue
            except RecursionError as re:
                print("bliskoznaczność - recursion error")

            # hiponimia
            try:
                foundtarg = wn.isIDConnectedWith(synset1.wnid, "n", "hiponimia", synset2.wnid)
                if foundtarg:
                    result.append((group[i][0], group[j][0], "hiponimia"))
                    continue
            except RecursionError as re:
                print("hiponimia - recursion error")

            # hiperonimia
            try:
                foundtarg = wn.isIDConnectedWith(synset1.wnid, "n", "hypernym", synset2.wnid)
                if foundtarg:
                    result.append((group[i][0], group[j][0], "hiperonimia"))
                    continue
            except RecursionError as re:
                print("hiperonimia - recursion error")

            # meronimia
            try:
                foundtarg = wn.isIDConnectedWith(synset1.wnid, "n", "meronimia", synset2.wnid)
                if foundtarg:
                    result.append((group[i][0], group[j][0], "meronimia"))
                    continue
            except RecursionError as re:
                print("meronimia - recursion error")

            # fuzzynimia synsetów
            try:
                foundtarg = wn.isIDConnectedWith(synset1.wnid, "n", "fuzzynimia synsetów", synset2.wnid)
                if foundtarg:
                    result.append((group[i][0], group[j][0], "fuzzynimia synsetów"))
                    continue
            except RecursionError as re:
                print("fuzzynimia synsetów - recursion error")

            # procesywność
            try:
                foundtarg = wn.isIDConnectedWith(synset1.wnid, "n", "procesywność", synset2.wnid)
                if foundtarg:
                    result.append((group[i][0], group[j][0], "procesywność"))
                    continue
            except RecursionError as re:
                print("procesywność - recursion error")
    return result


def semantic_relations(group_number):
    if group_number == 1:
        return get_s_m(group1)
    elif group_number == 2:
        return get_s_m(group2)


def get_sense_index(senses, synset):
    for i in range(0, len(senses)):
        if senses[i].wnid == synset.wnid:
            return i
    return -1


#literal = "wypadek drogowy" part_of_speech="n" relation = "hypernym"
def get_relation(literal, part_of_speech, relation, sense_number):
    senses = wn.lookUpLiteral(literal, part_of_speech)
    result = wn.lookUpSense(literal, sense_number, part_of_speech)
    sense_index = get_sense_index(senses, result)
    if not senses:
        print("Literal not found\n")
    else:
        #oss = wn.traceRelationOS(senses[sense_index].wnid, part_of_speech, relation)
        #result.extend(oss)
        root = Node(senses[sense_index].wnid)
        wn.traceRelationMine(root.id, part_of_speech, relation, root)
        for child in root.children:
            print(child.synonyms)
    return root


def get_hyponyms(parent, level):
    if level == 0:
        for child in parent.children:
            print(str(child.id) + " " + "{0}".format(child.synonyms))
    for child in parent.children:
        get_hyponyms(child, level-1)


def leacock_chodorow(literal1, sense1, literal2, sense2, part_of_speech, relation):
    synset1 = wn.lookUpSense(literal1, sense1, "n")
    synset2 = wn.lookUpSense(literal2, sense2, "n")
    return wn.simLeaCho(synset1.wnid, synset2.wnid, part_of_speech, relation, True)


def main():
    sys.setrecursionlimit(5000)
    root = get_relation("wypadek drogowy", "n", "hypernym", 1)
    my_graph = graph.make_graph(root)
    nx.draw(my_graph, with_labels=True)
    plt.show()
    root = get_relation("wypadek", "n", "hyponym", 1)
    print("direct hyponym")
    for child in root.children:
        print(str(child.id) + " " + "{0}".format(child.synonyms))
    print("2nd level hyponym")
    get_hyponyms(root, 1)
    res = semantic_relations(1)
    print("\n\n")
    for r in res:
        print(r)
    graph2 = graph.make_graph_from_array(res)
    d = {}
    for tuple in res:
        d[(tuple[0], tuple[1])] = tuple[2]
    pos = nx.spring_layout(graph2)
    nx.draw(graph2, with_labels=True, pos=pos)
    nx.draw_networkx_edge_labels(graph2, pos=pos, edge_labels=d)
    plt.show()

    res = semantic_relations(2)
    print("\n\n")
    for r in res:
        print(r)
    graph2 = graph.make_graph_from_array(res)
    d = {}
    for tuple in res:
        d[(tuple[0], tuple[1])] = tuple[2]
    print(d)
    pos = nx.spring_layout(graph2)
    nx.draw(graph2, with_labels=True, pos=pos)
    nx.draw_networkx_edge_labels(graph2, pos=pos, edge_labels=d)
    plt.show()

    first = leacock_chodorow("szkoda", 2, "wypadek", 1, "n", "hypernym")
    first2 = leacock_chodorow("szkoda", 2, "wypadek", 1, "n", "hyponym")
    second = leacock_chodorow("kolizja", 2, "szkoda majątkowa", 1, "n", "hypernym")
    second2 = leacock_chodorow("kolizja", 2, "szkoda majątkowa", 1, "n", "hyponym")
    third = leacock_chodorow("nieszczęście", 2, "katastrofa budowlana", 1, "n", "hypernym")
    third2 = leacock_chodorow("nieszczęście", 2, "katastrofa budowlana", 1, "n", "hyponym")
    print("szkoda-wypadek: {0} | kolizja-szkoda majątkowa: {1} | nieszczęście-katastrofa budowlana: {2}".format(first, second, third))
    print("szkoda-wypadek: {0} | kolizja-szkoda majątkowa: {1} | nieszczęście-katastrofa budowlana: {2}".format(first2, second2, third2))
main()
