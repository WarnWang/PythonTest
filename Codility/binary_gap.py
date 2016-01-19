#!/usr/bin/python
# -*- coding: utf-8 -*-

# File name: binary_gap
# Author: warn
# Date: 18/1/2016 22:01


def solution(N):
    zero_gap = bin(N).strip('0b')
    binary_gap = 0
    temp = 0
    for i in zero_gap:
        if i == '1':
            binary_gap = temp if temp > binary_gap else binary_gap
            temp = 0
        else:
            temp += 1
    return binary_gap
