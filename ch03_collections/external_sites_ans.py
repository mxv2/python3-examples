#!/usr/bin/env python3
import collections
import sys

sites = collections.defaultdict(set)
for filename in sys.argv[1:]:
    for line in open(filename):
        i = 0
        while True:
            site = None
            i = line.find("http://", i)
            if i > -1:
                i += len("http://")
                j = 0
                for j in range(i, len(line)):
                    if not (line[j].isalnum() or line[j] in ".-"):
                        site = line[i:j].lower()
                        break
                if site and "." in site:
                    sites[site].add(filename)
                i = j
            else:
                break

print(sites)
