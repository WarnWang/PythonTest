#!/usr/bin/python
# -*- coding: utf-8 -*-

# File name: odd_occurance_in_array
# Author: warn
# Date: 19/1/2016 15:20

import math


def solution(A):
    temp = 0
    for i in A:
        temp ^= i

    return temp


if __name__ == '__main__':
    print solution([1, 2, 1, 9, 9, 8, 2])
