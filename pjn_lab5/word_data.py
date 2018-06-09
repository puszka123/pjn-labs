

class Word:
    def __init__(self, word, pos):
        self.word = word
        self.pos = pos

    def __str__(self):
        return self.word + ":" + self.pos


class Bigram:
    def __init__(self, word1, word2):
        self.word1 = word1
        self.word2 = word2

    def __str__(self):
        return str(self.word1) + " " + str(self.word2)
