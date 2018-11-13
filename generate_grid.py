#!/usr/bin/env python3

import random

def prompt_int(msg, minimum, default):
    while True:
        try:
            line = input(msg)
            if not line and default is not None:
                return default
            i = int(line)
            if i < minimum:
                print("must be >=", minimum)
            else:
                return i
        except ValueError as err:
            print(err)
    
rows = prompt_int("rows: ", 1, None)
columns = prompt_int("columns: ", 1, None)
minimum = prompt_int("minimum (or Enter for 0): ", -1000000, 0)

default = 1000
if default < minimum:
    default = minimum * 2
maximum = prompt_int("maximum (or Enter for " + str(default) + "): ", minimum, default)

row = 0
while row < rows:
    line = ""
    column = 0
    while column < columns:
        number = random.randint(minimum, maximum)
        number_str = str(number)
        while len(number_str) < 10:
            number_str = " " + number_str
        line += number_str + " "
        column += 1
    print(line)
    row += 1

