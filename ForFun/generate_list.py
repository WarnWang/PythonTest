#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Project: PythonTest
# File name: generate_list
# Author: Mark Wang
# Date: 4/5/2016


import random


def get_large_list(length=100, minimum=1, maximum=10):
    large_list = []
    for _ in range(length):
        large_list.append(random.randrange(start=minimum, stop=maximum))

    return large_list


if __name__ == '__main__':
    print get_large_list(length=25000)
