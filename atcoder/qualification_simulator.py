#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Project: PythonTest
# File name: qualification_simulator
# Author: Mark Wang
# Date: 10/10/2016

"""
Problem Statement
There are N participants in the CODE FESTIVAL 2016 Qualification contests. The participants are either students in Japan, students from overseas, or neither of these.

Only Japanese students or overseas students can pass the Qualification contests. The students pass when they satisfy the conditions listed below, from the top rank down. Participants who are not students cannot pass the Qualification contests.

A Japanese student passes the Qualification contests if the number of the participants who have already definitively passed is currently fewer than A+B.
An overseas student passes the Qualification contests if the number of the participants who have already definitively passed is currently fewer than A+B and the student ranks B-th or above among all overseas students.
A string S is assigned indicating attributes of all participants. If the i-th character of string S is a, this means the participant ranked i-th in the Qualification contests is a Japanese student; b means the participant ranked i-th is an overseas student; and c means the participant ranked i-th is neither of these.

Write a program that outputs for all the participants in descending rank either Yes if they passed the Qualification contests or No if they did not pass.

Constraints
1≦N,A,B≦100000
A+B≦N
S is N characters long.
S consists only of the letters a, b and c.
"""

input1 = raw_input()
s = raw_input()

n, a, b = map(int, input1.split(' '))

n_a, n_b = 0, 0

for i in range(n):
    c = s[i]
    if c == 'a':
        n_a += 1
        if n_a + n_b <= a + b:
            print 'Yes'
        else:
            print 'No'

    elif c == 'b':
        n_b += 1
        if n_a + n_b <= a + b and n_b <= b:
            print 'Yes'
        else:
            print 'No'
    elif c == 'c':
        print 'No'
