#!/usr/bin/env python3

print("Type integers, each followed by Enter; or just Enter to finish")

numbers = []
sum = 0
lowest = 0
highest = 0

while True:
    s = input("number: ")
    if not s:
        break
    try:
        num = int(s)
        if len(numbers) == 0 or num < lowest:
            lowest = num
        if len(numbers) == 0 or num > highest:
            highest = num
        numbers.append(num)
        sum += num
    except ValueError as err:
        print(err)
        continue

if not numbers:
    print("noting to calculate")
else:
    print("numbers:", numbers)
    print("count = {count} sum = {sum} lowest = {lowest} highest = {highest} mean = {mean}".format(
            count=len(numbers),
            sum=sum,
            lowest=lowest,
            highest=highest,
            mean=sum/len(numbers)
    ))

