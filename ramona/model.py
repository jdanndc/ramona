#
# third order markov chains, word trigrams
#
import nltk
import random
from collections import defaultdict
from itertools import groupby
import numpy as np

class Model(object):
    # sentinel to mark beginning of sentence
    bos_sentinel = "^^^^^"

    def __init__(self):
        self.reset()

    def reset(self):
        self.states = None
        self.start_states = None
        self.counts = defaultdict(lambda: defaultdict(int))
        return self

    def add_text(self, text, bos=True):
        """Process text string and fill counts dict with token trigrams

        :param text: a string of text to sentencize and tokenize
        :return: None
        """
        for sent in nltk.sent_tokenize(text):
            tokens = nltk.word_tokenize(sent)
            if bos:
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


