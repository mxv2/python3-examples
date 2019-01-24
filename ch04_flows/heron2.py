import math


def heron(a, b, c, *, units="square meters"):
    """Calculates and prints area of a triangle
    from sides by Heron's formula

    :param a: side a
    :param b: side b
    :param c: side c
    :param units: desired units for printing
    :return:
    """
    s = (a + b + c) / 2
    area = math.sqrt(s * (s - a) * (s - b) * (s - c))
    return "{0} {1}".format(area, units)
