#!/usr/bin/env python3
import cmath
import math
import sys


def is_float_zero(x):
    return abs(x) < sys.float_info.epsilon


def sign(x):
    if x < 0:
        return "-"
    return "+"


def get_float(msg, allow_zero):
    x = None
    while x is None:
        try:
            x = float(input(msg))
            if not allow_zero and is_float_zero(x):
                x = None
                print("zero is not allowed")
            else:
                return x
        except ValueError as err:
            print(err)


print("ax\N{SUPERSCRIPT TWO} + bx + c = 0")

a = get_float("enter a: ", False)
b = get_float("enter b: ", True)
c = get_float("enter c: ", True)

x1 = None
x2 = None
discriminant = (b ** 2) - (4 * a * c)
if discriminant == 0:
    x1 = -b / (2 * a)
else:
    if discriminant > 0:
        root = math.sqrt(discriminant)
    else:
        root = cmath.sqrt(discriminant)
    x1 = (-b + root) / (2 * a)
    x2 = (-b - root) / (2 * a)

equation = ""
if not is_float_zero(a):
    equation += "{}x\N{SUPERSCRIPT TWO}".format(a)
if not is_float_zero(b):
    equation += " {} {}x".format(sign(b), abs(b))
if not is_float_zero(c):
    equation += " {} {}".format(sign(c), abs(c))
equation += " = 0 \N{RIGHTWARDS ARROW} x = {}".format(x1)
if x2 is not None:
    equation += " or x = {}".format(x2)

print(equation)
