import re

class Node:
    def __init__(self, id):
        self.id = id
        self.children = []
        self.synonyms = None
        self.definition = ""

    def add_child(self, child):
        self.children.append(Node(child))

    def add_children(self, children):
        for child in children:
            self.add_child(child)

    def get_child_by_id(self, id):
        for child in self.children:
            if child.id == id:
                return child
        return None

    def get_name(self):
        return str(self.id) + " " + self.synonyms[0]
