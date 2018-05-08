import networkx as nx
from node import Node


def make_graph(root):
    graph = nx.DiGraph()
    build(graph, root)
    return graph


def build(graph, parent):
    graph.add_node(parent.get_name())
    for child in parent.children:
        graph.add_node(child.get_name())
        graph.add_edge(parent.get_name(), child.get_name())
        build(graph, child)


def make_graph_from_array(array):
    graph = nx.DiGraph()
    used_words = []
    for tuple in array:
        if not tuple[0] in used_words:
            graph.add_node(tuple[0])
            used_words.append(tuple[0])
        if not tuple[1] in used_words:
            graph.add_node(tuple[1])
            used_words.append(tuple[1])
        graph.add_edge(tuple[0], tuple[1])
    return graph
