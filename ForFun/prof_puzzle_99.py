#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Project: PythonTest
# File name: prof_puzzle_99
# Author: Mark Wang
# Date: 7/6/2016


def get_possible_num(remain_number=None, num1=None, num2=None):
    if remain_number is None:
        remain_number = range(1, 10)

    if num1 is None:
        num1 = []
    if num2 is None:
        num2 = []

    if not remain_number:
        a1 = int("".join(map(str, num1))) - int("".join(map(str, num2)))
        if a1 == 33333:
            print num1
            print num2

    elif len(num1) == 5:
        for i in remain_number:
            another_remain = remain_number[:]
            another_remain.remove(i)
            num2_ = num2[:]
            num2_.append(i)
            get_possible_num(another_remain, num1[:], num2_)
    else:
        for i in remain_number:
            another_remain = remain_number[:]
            another_remain.remove(i)
            num1_ = num1[:]
            num1_.append(i)
            get_possible_num(another_remain, num1_, num2[:])


if __name__ == "__main__":
    get_possible_num()
