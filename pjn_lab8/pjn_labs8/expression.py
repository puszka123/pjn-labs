import re

class Expression:
    def __init__(self, token_name, classification_name, class_index):
        self.class_name = classification_name
        self.tokens = []
        self.tokens.append(token_name)
        self.class_index = class_index
        r = re.split(r'_', classification_name)
        self.general_class_name = r[0]+'_'+r[1]

    def __str__(self):
        tokens = ''
        for token in self.tokens:
            tokens += token + ' '
        return self.class_name + ' ' + tokens

    def get_tokens(self):
        tokens = ''
        for token in self.tokens:
            tokens += token + ' '
        return tokens.strip()
