#!/usr/bin/env python3
import collections
import string
import sys


def get_entry_value(entry):
    return entry[1]


words = collections.defaultdict(int)
strip = string.whitespace + string.punctuation + string.digits + "\"'"
for filename in sys.argv[1:]:
    for line in open(filename):
        for word in line.lower().split():
            word = word.strip()
            if len(word) > 2:
                words[word] += 1

for word, frequency in sorted(words.items(), key=get_entry_value, reverse=True):
    print("{0} occurs {1} times".format(word, frequency))
