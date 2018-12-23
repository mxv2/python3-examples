#!/usr/bin/env python3

import random
import utils

_ARTICLES = ("the", "a")
_SUBJECTS = ("cat", "dog", "man", "woman")
_VERBS = ("sang", "ran", "jumped")
_ADVERBS = ("loudly", "quietly", "well", "badly")

_STRUCTURES = [
    [_ARTICLES, _SUBJECTS, _VERBS, _ADVERBS],
    [_ARTICLES, _SUBJECTS, _VERBS]
]

max_sentences = 0
while 1 > max_sentences < 10:
    max_sentences = utils.prompt_int("how much sentences:", 1, 5, 10)

count = 0
while count < max_sentences:
     structure = _STRUCTURES[random.randint(0, 1)]
     sentence = ""
     for token in structure:
         sentence += random.choice(token) + " "
     print(sentence)
     count += 1

