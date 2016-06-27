#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Project: PythonTest
# File name: test_char
# Author: Mark Wang
# Date: 27/6/2016


def test_char(row_index):
    row_char = ''
    while row_index / 26 > 0:
        row_char = '{1}{0}'.format(row_char, chr(ord('A') + (row_index % 26)))
        row_index = row_index / 26 - 1

    row_char = '{1}{0}'.format(row_char, chr(ord('A') + (row_index % 26)))
    return row_char


if __name__ == "__main__":
    for i in range(676, 767):
        print test_char(i)
