#!/usr/bin/python
# -*- coding: utf-8 -*-

# Project: PythonTest
# File name: combination_caluculate
# Author: Mark Wang
# Date: 19/3/2016

import math


def combination(n, k):
    result = 1
    times = min(k, n - k)
    for i in range(1, times + 1):
        result *= (n - i + 1)
        result /= i

    return result


# Are you smart enough to work at Google p67
# Nth step
def stair_steps(n):
    times = 0
    if n & 1 == 1:
        for i in range((n + 1) / 2):
            times += combination(n - i, i)
    else:
        for i in range((n >> 1) + 1):
            times += combination(n - i, i)

    return times


if __name__ == "__main__":
    # print combination(2, 0)
    for i in range(1, 11):
        print stair_steps(i)
