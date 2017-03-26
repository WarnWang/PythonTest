#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Project: PythonTest
# File name: matrix_test_code
# Author: warn
# Date: 2017/3/25

import pycuda.autoinit
import pycuda.driver as drv
import numpy as np

from CUDATest.numba_code.matrix_dot import mulpy_matrix
from CUDATest.pycuda_code.matrix_dot import multiply_them
from CUDATest.utilities import timefunc

MATRIX_SIZE = 20

a = np.random.randn(MATRIX_SIZE, MATRIX_SIZE).astype(np.float32)
b = np.random.randn(MATRIX_SIZE, MATRIX_SIZE).astype(np.float32)

dest = np.zeros_like(a).astype(np.float32)
dest1 = np.zeros_like(a).astype(np.float32)

timefunc(None, "PyCUDA Code", multiply_them,
         drv.Out(dest), drv.In(a), drv.In(b),
         block=(MATRIX_SIZE, MATRIX_SIZE, 1), grid=(1, 1))

dest1 = timefunc(dest, 'NUMBA Code Single', mulpy_matrix, dest1, a, b)

print(dest - dest1)
