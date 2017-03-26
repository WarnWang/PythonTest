#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Project: PythonTest
# File name: matrix_dot
# Author: warn
# Date: 2017/3/25

from numba import jit


# jit decorator tells Numba to compile this function.
# The argument types will be inferred by Numba when function is called.
@jit('float32[:,:](float32[:,:], float32[:,:], float32[:,:])')
def mulpy_matrix(result, arr1, arr2):
    M, N = arr1.shape
    for i in range(M):
        for j in range(N):
            result[i, j] += arr1[i, j] * arr2[i, j]

    return result


if __name__ == '__main__':
    import numpy as np

    a = np.random.randn(400, 400).astype(np.float32)
    b = np.random.randn(400, 400).astype(np.float32)
    result = np.zeros_like(a).astype(np.float32)

    mulpy_matrix(result, a, b)

    print(a * b - result)
