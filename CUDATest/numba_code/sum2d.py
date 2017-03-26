#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Project: PythonTest
# File name: sum2d
# Author: warn
# Date: 2017/3/25

from numba import jit
from numpy import arange


# jit decorator tells Numba to compile this function.
# The argument types will be inferred by Numba when function is called.
@jit
def sum2d(arr):
    M, N = arr.shape
    result = 0.0
    for i in range(M):
        for j in range(N):
            result += arr[i, j]
    return result


a = arange(9).reshape(3, 3)
print(sum2d(a))
