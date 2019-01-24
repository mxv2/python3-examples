#!/usr/bin/env python3
import sys

Language = "en"

ENGLISH = {0: "zero", 1: "one", 2: "two", 3: "three", 4: "four",
           5: "five", 6: "six", 7: "seven", 8: "eight", 9: "nine"}
FRENCH = {0: "zéro", 1: "un", 2: "deux", 3: "trois", 4: "quatre",
           5: "cinq", 6: "six", 7: "sept", 8: "huit", 9: "neuf"}


def print_digit(number):
    dictionary = ENGLISH if Language == "en" else FRENCH
    for digit in number:
        print(dictionary[int(digit)], end=" ")
    print()


def main():
    if len(sys.argv) == 1 or sys.argv[1] in ("-h", "--help"):
        print("usage: {0} [en|fr] number".format(sys.argv[0]))
        sys.exit()

    args = sys.argv[1:]
    if args[0] in ("en", "fr"):
        global Language
        Language = args.pop(0)
    print_digit(args.pop(0))


main()
