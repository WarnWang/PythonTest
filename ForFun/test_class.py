#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Project: PythonTest
# File name: test_class
# Author: Mark Wang
# Date: 9/5/2016

def act_func(x):
    import numpy as np
    y = np.array(x, dtype=np.float64)
    return 1.0 / np.exp(x, y)


class OnlyForFun(object):
    def __init__(self):
        act_func = lambda x: x ** 2

    def calculate(self):
        print act_func(5)


if __name__ == "__main__":
    # test = OnlyForFun()
    # test.calculate()
    print globals()['act_func'](1)
