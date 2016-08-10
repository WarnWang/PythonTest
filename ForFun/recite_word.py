#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Project: PythonTest
# File name: recite_word
# Author: Mark Wang
# Date: 10/8/2016

import random

total = range(1, 32, 1)
uncover = [1, 3, 6, 7, 8, 9, 11, 12, 16, 18, 25, 27, 28, 30]

covered = set(total).difference(set(uncover))
print covered
print uncover

print "Today's task", random.choice(uncover)
print "Review task", random.choice(list(covered))
