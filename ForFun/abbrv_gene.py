#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Project: PythonTest
# File name: abbrv_gene
# Author: Mark Wang
# Date: 25/6/2016


s = '''ANN Artificial Neural Network
MACD Moving average convergence divergence
SVM Support Vector Machines
ROC Rate Of Change
RSI Relative Strength Index
HIBOR Hang Seng Interbank Offered Rate
HKD Hong Kong Dollar
EMH Efficient Market Hypothesis
HKEX Hong Kong Exchanges and clearing Limited
PCA Principal Components Analysis'''


def format_first_word(word):
    return '\\textbf{%s}' % word


def format_first_letter(word):
    return '\\textbf{%s}%s' % (word[0], word[1:])


new_list = []
for line in s.split('\n'):
    words = line.split(' ')
    s2 = '%s &' % format_first_word(word=words[0])
    for i in range(1, len(words)):
        s2 = '%s %s' % (s2, format_first_letter(words[i]))
    new_list.append(s2)

print '\\\\\n'.join(new_list)
