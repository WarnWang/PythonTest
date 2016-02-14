#!/usr/bin/python
# -*- coding: utf-8 -*-

# File name: fibonacci
# Author: warn
# Date: 4/2/2016 18:41


def get_fibonacci(n):
    a1 = 1
    a2 = 1
    while a2 < n:
        print a2
        a1, a2 = a2, a1 + a2


if __name__ == "__main__":
    get_fibonacci(1000000)
