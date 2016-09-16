#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Project: PythonTest
# File name: practise
# Author: Mark Wang
# Date: 16/9/2016

one_int = raw_input()
two_int = raw_input()
sum_int = int(one_int) + sum(map(int, two_int.split(' ')))
input_str = raw_input()
print sum_int, input_str
