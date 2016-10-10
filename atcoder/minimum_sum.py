#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Project: PythonTest
# File name: minimum_sum
# Author: Mark Wang
# Date: 1/10/2016

"""
One day, Snuke was given a permutation of length N, a1,a2,…,aN, from his friend.

Find the following:

Constraints
1≦N≦200,000
(a1,a2,…,aN) is a permutation of (1,2,…,N).
"""

n = int(raw_input())
permutation_str = raw_input()
permutation_list = map(int, permutation_str.split(' '))
permutation_sum = permutation_list[0]
prior_list = [permutation_list[0]]
