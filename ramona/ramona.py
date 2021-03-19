#
# word trigrams - third order
#
import nltk
import random
from collections import defaultdict
from itertools import groupby
import numpy as np

class Ramona(object):
    # sentinel to mark beginning of sentence
    bos_sentinel = "^^^^^"

    def __init__(self):
        self.states = None
        self.start_states = None
        self.counts = defaultdict(lambda: defaultdict(int))
        pass

    def add_text(self, text):
        """Process text string and fill counts dict with token trigrams

        :param text: a string of text to sentencize and tokenize
        :return: None
        """
        for sent in nltk.sent_tokenize(text):
            tokens = nltk.word_tokenize(sent)
            tokens.insert(0, self.bos_sentinel)
            trigrams = sorted(list(zip(tokens, tokens[1:], tokens[2:])))  # all dimensions get sorted
            for k, g in groupby(trigrams, lambda x: (x[0], x[1])):
                for k2, g2 in groupby(g, lambda x: x[2]):
                    self.counts[k][k2] += len(list(g2))
        return self

    def recalculate(self):
        self.states = {}
        for k,v in self.counts.items():
            n = sum(v.values())
            words=[]
            probs=[]
            for k2,v2 in v.items():
                words.append(k2)
                probs.append(v2/n)
            self.states[k] = (words, probs)
        self.start_states = [x[0:2] for x in self.states.keys() if x[0] == self.bos_sentinel]
        return self

    def generate(self):
        out = []
        not_done = True
        curr_state = random.choice(self.start_states)
        MAX_ITERS = 1500
        iter = 0
        while iter < MAX_ITERS:
            if curr_state not in self.states.keys():
                out.extend(curr_state)
                out.append("\n")
                break
            if curr_state[0] != self.bos_sentinel:
                out.append(curr_state[0])
            randompick = np.random.multinomial(1, self.states[curr_state][1])
            idx = list(randompick).index(1)
            curr_state = (curr_state[1], self.states[curr_state][0][idx])
            iter += 1
        return out

# all in one line
#print(' '.join(Ramona().add_text(open('data/gatsby.txt').read()).recalculate().generate()))

ramona = Ramona()
ramona.add_text(open('data/ethan_frome.txt').read())
ramona.add_text(open('data/theron_ware.txt').read())
ramona.add_text(open('data/gatsby.txt').read())
ramona.recalculate()

for i in range(0,20):
    print(' '.join(ramona.generate()))

