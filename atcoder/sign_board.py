#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Project: PythonTest
# File name: sign_board
# Author: Mark Wang
# Date: 10/10/2016

"""
Problem Statement
CODE FESTIVAL 2016 is going to be held. For the occasion, Mr. Takahashi decided to make a signboard.

He intended to write CODEFESTIVAL2016 on it, but he mistakenly wrote a different string S. Fortunately, the string he wrote was the correct length.

So Mr. Takahashi decided to perform an operation that replaces a certain character with another in the minimum number of iterations, changing the string to CODEFESTIVAL2016.

Find the minimum number of iterations for the rewrite operation.

Constraints
S is 16 characters long.
S consists of uppercase and lowercase alphabet letters and numerals.
"""

target = 'CODEFESTIVAL2016'

s = raw_input()
count = 0

for i in range(len(s)):
    if s[i] != target[i]:
        count += 1

print count
