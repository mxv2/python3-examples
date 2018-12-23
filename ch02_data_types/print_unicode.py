#!/usr/bin/env python3
import sys

import unicodedata


def print_unicode(word):
    print("{0:^7} {1:^5} {2:^5} {3:^40}".format("decimal", "hex", "chr", "name"))
    print("{0:-^7} {0:-^5} {0:-^5} {0:-^40}".format(""))

    code = ord(" ")
    last_char = sys.maxunicode

    while code < last_char:
        ch = chr(code)
        name = unicodedata.name(ch, "unknown name")
        if not word or word in name.lower():
            try:
                print("{0:7} {0:5X} {0:^5c} {1:<40}".format(code, name.title()))
            except UnicodeEncodeError:
                pass
        code += 1


word = None
if len(sys.argv) > 1:
    argument = sys.argv[1]
    if argument in ("-h", "--help"):
        print("usage: {0} <word>".format(sys.argv[0]))
        word = 0
    else:
        word = argument.lower()
if word != 0:
    print_unicode(word)
