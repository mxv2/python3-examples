#!/usr/bin/env python3

import random

_ARTICLES = ("the", "a")
_SUBJECTS = ("cat", "dog", "man", "woman")
_VERBS = ("sang", "ran", "jumped")
_ADVERBS = ("loudly", "quietly", "well", "badly")

_STRUCTURES = [
    [_ARTICLES, _SUBJECTS, _VERBS, _ADVERBS],
    [_ARTICLES, _SUBJECTS, _VERBS]
]

count = 0
while count < 5:
     structure = _STRUCTURES[random.randint(0, 1)]
     sentence = ""
     for token in structure:
         sentence += random.choice(token) + " "
     print(sentence)
     count += 1

