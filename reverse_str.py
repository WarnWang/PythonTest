#!/usr/bin/python
# -*- coding: utf-8 -*-

# Project: PythonTest
# File name: reverse_str
# Author: Mark Wang
# Date: 17/3/2016


def reverse_tradition_version(string_input):
    return "".join(reversed(string_input))


def reverse_version_1(string_input):
    n = len(string_input)
    new_str = []
    for i in range(n):
        new_str.append(string_input[n - i - 1])

    return "".join(new_str)


def reverse_version_2(string_input):
    new_str = list(string_input)
    start_index = 0
    end_index = len(new_str) - 1
    while start_index <= end_index:
        new_str[start_index], new_str[end_index] = new_str[end_index], new_str[start_index]
        start_index += 1
        end_index -= 1

    return "".join(new_str)


def reverse_version_3(string_input):
    new_str = ""
    for i in range(len(string_input) - 1, -1, -1):
        # new_str = "%s%s" % (new_str, string_input[i])
        new_str = "{}{}".format(new_str, string_input[i])

    return new_str
