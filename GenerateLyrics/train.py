#!/usr/bin/env python
# coding: utf-8

"""author = Necva BÖLÜCÜ"""

import dynet as dy
import time
import random
import numpy as np
import string
import re
import util
from collections import Counter
from sys import argv
import math

from collections import defaultdict

BEG_SEQ = "<S>"
END_SEQ = "</S>"
UNK = "_UNK_"
NEW_LINE = "_NEWLINE_"


def read_dataset(filename):
    sentences = []
    words = []

    sentence = ""
    with open(filename, "r", encoding="utf8") as f:
        song = BEG_SEQ + " "
        for line in f:
            if "/sarkici" in line:
                song = song[:-10]
                song += END_SEQ
                sentences.append(song)
                words.extend(song.split())
                song = BEG_SEQ + " "
            else:
                line = line.lower().strip().strip("\n")
                line = line.translate(str.maketrans('', '', string.punctuation))
                song += line + " " + NEW_LINE + " "
                
    return sentences, set(words)

sentences,words = read_dataset("songAll1.txt")





words = []
wc = Counter()
for sent in sentences:
    for word in sent.split():
        words.append(word)
        wc[word] += 1
          

words.append(UNK)
words.append(NEW_LINE)
words.append(BEG_SEQ)
words.append(END_SEQ)

vw = util.Vocab.from_corpus([words])
UNKK = vw.w2i[UNK]
BEG_SEQQ = vw.w2i[BEG_SEQ]
END_SEQQ = vw.w2i[END_SEQ]
NEW_LINEE = vw.w2i[NEW_LINE]
nwords = vw.size()

model = dy.Model()


params = {}


# then, when loading:
pc2 = dy.ParameterCollection()
params["lookup"],params["R"],params["bias"],lstm = dy.load("lm-LSTM-song-1500-3", pc2)
        

#lstm = dy.LSTMBuilder(LAYERS, INPUT_DIM, HIDDEN_DIM, model)
#lstm.set_dropout(dropout)        

# generate from model:
def generate_lyrics_from_model(lstm, line_condition, word_condition):
    file_name = argv[1]
    def sample(probs):
        rnd = random.random()
        for i,p in enumerate(probs):
            rnd -= p
            if rnd <= 0: break
        return i

    # setup the sentence
    dy.renew_cg()
    s0 = lstm.initial_state()

    R = dy.parameter(params["R"])
    bias = dy.parameter(params["bias"])
    lookup = params["lookup"]

    s = s0.add_input(lookup[vw.w2i.get(BEG_SEQ)])
    out = []
    new_line_count = 0
    word_count = 0
    loss = 1
    while True:
        probs = dy.softmax(R*s.output() + bias)
        probs = probs.vec_value()
        next_word = sample(probs)
        next_wordd = vw.i2w.get(next_word)
        loss += math.exp(probs[next_word])
        word_count += 1
        if next_wordd == NEW_LINE:
            new_line_count += 1
            out.append('\n')
        if next_wordd != NEW_LINE and next_wordd != '</S>':
            out.append(next_wordd + " ")
        if out[-1] == END_SEQ or new_line_count == line_condition: break
        s = s.add_input(lookup[next_word])
    print(loss)
    outfile = open("../example/lyrics/" + file_name + "_lyrics.txt", 'w')
    outfile.write("".join(out))
    outfile.close()
    return " ".join(out), loss # strip the <EOS>





gerenerated_sentence = generate_lyrics_from_model(lstm,12,200)

