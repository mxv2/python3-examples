#!/usr/bin/env python3
import sys


def product(*args):
    assert all(args), "any 0 arguments"
    result = 1
    for arg in args:
        result *= arg
    return result


def main():
    if len(sys.argv) == 1 or sys.argv[1] in ("-h", "--help"):
        print("usage: {0} number [numbers]".format(sys.argv[0]))
        sys.exit()

    numbers = []
    for arg in sys.argv[1:]:
        numbers.append(int(arg))
    print("product = {0}".format(product(*numbers)))


main()
