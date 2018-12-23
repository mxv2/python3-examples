#!/usr/bin/env python3


def merge_sort(arr, left, right):
    distance = right - left
    if distance == 0:
        return [arr[left]]

    middle = int((left + right) / 2)
    left_part = merge_sort(arr, left, middle)
    right_part = merge_sort(arr, middle + 1, right)

    lp_index, rp_index = 0, 0
    merged_arr = []
    while lp_index < len(left_part) and rp_index < len(right_part):
        left_element = left_part[lp_index]
        right_element = right_part[rp_index]

        if left_element <= right_element:
            merged_arr.append(left_element)
            lp_index += 1
        else:
            merged_arr.append(right_element)
            rp_index += 1

    while lp_index < len(left_part):
        left_element = left_part[lp_index]
        merged_arr.append(left_element)
        lp_index += 1

    while rp_index < len(right_part):
        right_element = right_part[rp_index]
        merged_arr.append(right_element)
        rp_index += 1

    return merged_arr


print("Type integers, each followed by Enter; or just Enter to finish")

numbers = []

while True:
    s = input("number: ")
    if not s:
        break
    try:
        num = int(s)
        numbers.append(num)
    except ValueError as err:
        print(err)

if not numbers:
    print("noting to calculate")
else:
    print("numbers:", numbers)
    numbers = merge_sort(numbers, 0, len(numbers)-1)
    print("sorted:", numbers)

    length = len(numbers)
    middle = int(length / 2)
    if length % 2 == 0:
        mean = (numbers[middle] + numbers[middle-1]) / 2
    else:
        mean = numbers[middle]
    print(" mean = " + str(mean))
