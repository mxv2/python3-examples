#!/usr/bin/env python3
import collections
import math
import sys

MAX_NODES = 3

Statistics = collections.namedtuple("Statitistics",
                                    "count mean median mode std_dev")


def main():
    if len(sys.argv) == 1 or sys.argv[1] in ("-h", "--help"):
        print("usage: {0} file1 [file2 [... fileN]]".format(sys.argv[0]))
        sys.exit()

    numbers = []
    frequencies = collections.defaultdict(int)
    for filename in sys.argv[1:]:
        read_data(filename, frequencies, numbers)

    statistics = calculate_statistics(frequencies, numbers)
    print_statistics(statistics)


def print_statistics(statistics):
    real = "9.2f"
    
    if statistics.mode is None:
        modeline = ""
    elif len(statistics.mode) == 1:
        modeline = "mode      = {0:{fmt}}\n".format(
            statistics.mode[0], fmt=real
        )
    else:
        modeline = ("mode      = [" +
                    ",".join(["{0:.2f}".format(m) for m in statistics.mode]) +
                    "]\n")
    print("""\
    count     = {count:6}
    mean      = {mean:{fmt}}
    median    = {median:{fmt}}
    {modeline}\
    std. dev. = {std_dev:{fmt}}""".format(
        modeline=modeline, fmt=real, **statistics._asdict()
    ))


def calculate_statistics(frequencies, numbers):
    count = len(numbers)
    mean = sum(numbers) / count
    median = calculate_median(count, numbers)
    mode = calculate_mode(frequencies, MAX_NODES)
    std_dev = calculate_standard_deviation(count, mean, numbers)
    return Statistics(count, mean, median, mode, std_dev)


def calculate_standard_deviation(count, mean, numbers):
    sum_quad_dev = sum([(number - mean) ** 2 for number in numbers])
    std_dev = math.sqrt(sum_quad_dev / (count - 1))
    return std_dev


def calculate_mode(frequencies, maximum_nodes):
    highest_frequency = max(frequencies.values())
    mode = [number for number, count in frequencies.items() if count == highest_frequency]
    if len(mode) > maximum_nodes:
        mode = None
    return mode


def calculate_median(count, numbers):
    sn = sorted(numbers)
    middle = count // 2
    median = sn[middle]
    if count % 2 == 0:
        median = (median + sn[middle - 1]) / 2
    return median


def read_data(filename, frequencies, numbers):
    for lino, line in enumerate(open(filename, encoding="ascii"),
                                start=1):
        for x in line.split():
            try:
                number = float(x)
                numbers.append(number)
                frequencies[number] += 1
            except ValueError as err:
                print("{filename}:{lino}: skipping {x}: {err}".format(
                    **locals()
                ))


main()
