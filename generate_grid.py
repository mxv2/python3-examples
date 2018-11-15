#!/usr/bin/env python3

import random
import utils

rows = utils.prompt_int("rows: ", 1, None)
columns = utils.prompt_int("columns: ", 1, None)
minimum = utils.prompt_int("minimum (or Enter for 0): ", -1000000, 0)

default = 1000
if default < minimum:
    default = minimum * 2
maximum = utils.prompt_int("maximum (or Enter for " + str(default) + "): ", minimum, default)

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

