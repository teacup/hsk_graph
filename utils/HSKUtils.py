#!/usr/bin/env python
# -*- coding: utf-8 -*-

from collections import Counter, defaultdict

from ..hanzidata import HSKHanzi


def countCharacters(amount, hanziData):
    return len(Counter(key for key in hanziData if len(key) == amount))


def countCharacters2(amount, hanziData):
    counts = defaultdict(int)
    for x in sequence:
        counts[x] += 1
    return counts


def isHanzi(character):
    # parameter: One character String
    # returns: Boolean

    # ord() only takes single characters
    return any([start <= ord(character) <= end for start, end in
                [(4352, 4607), (11904, 12287), (12544, 12591), (12688, 12783), (12800, 42191),
                 (43072, 43135), (63744, 64255), (65072, 65103), (131072, 196607)]
                ])


def isAllHanzi(hanzi):
    # parameter: String
    # returns: Boolean

    return all(isHanzi(character) for character in list(hanzi))


def hSKLevel(hanzi):
    # parameter: (UTF8?) String
    # returns: Int，1-6= HSK levels, 7= Not in HSK 

    levels = []
    hanzi.encode("utf-8")

    # search for individual characters within keys as well as full keys    
    for key in HSKHanzi.keys():
        if hanzi in key:
            levels.append(HSKHanzi[key])
        else:
            continue

    # return lowest HSK level which contains character    
    if len(levels) > 0:
        return min(levels)
    else:
        return 7
