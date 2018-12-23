#!/usr/bin/env python3

print("Type integers, each followed by Enter; or just Enter to finish")

count = 0
sum = 0

while True:
    s = input("number: ")
    if not s:
        break
    try:
        num = int(s)
    except ValueError:
        print("invalid literal for int() with base 10: '{literal}'".format(literal=s))
        continue
    count += 1
    sum += num

if count == 0:
    print("noting to calculate")
else:
    print("count = {count}, sum = {sum}, mean = {mean}".format(
            count=count,
            sum=sum,
            mean=sum/count
    ))

