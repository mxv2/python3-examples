#!/usr/bin/env python3
import sys

import unicodedata


def print_unicode(words):
    print("{0:^7} {1:^5} {2:^5} {3:^40}".format("decimal", "hex", "chr", "name"))
    print("{0:-^7} {0:-^5} {0:-^5} {0:-^40}".format(""))

    code = ord(" ")
    last_char = sys.maxunicode

    while code < last_char:
        ch = chr(code)
        name = unicodedata.name(ch, "unknown name")
        if not words or is_words_in_string(name.lower(), words):
            try:
                print("{0:7} {0:5X} {0:^5c} {1:<40}".format(code, name.title()))
            except UnicodeEncodeError:
                pass
        code += 1


def is_words_in_string(string, words):
    for word in words:
        if word not in string:
            return False
    return True


words = []
if len(sys.argv) > 1:
    arguments = sys.argv[1:]
    if arguments[0] in ("-h", "--help"):
        print("usage: {0} <word>...".format(sys.argv[0]))
        words = None
    else:
        for arg in arguments:
            words.append(arg.lower())
if words is not None:
    print_unicode(words)
