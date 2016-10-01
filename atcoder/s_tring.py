#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Project: PythonTest
# File name: s_tring
# Author: Mark Wang
# Date: 1/10/2016

# We have a string X, which has an even number of characters. Half the characters are S, and the other half are T.
#
# Takahashi, who hates the string ST, will perform the following operation 1010000 times:
#
# Among the occurrences of ST in X as (contiguous) substrings, remove the leftmost one. If there is no occurrence, do
# nothing.
# Find the eventual length of X.

input_string = raw_input()

s_num = 0
str_len = len(input_string)

for c in input_string:
    if c == 'S':
        s_num += 1

    elif c == 'T':
        if s_num > 0:
            s_num -= 1
            str_len -= 2

print str_len
