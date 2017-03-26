#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Project: PythonTest
# File name: matrix_dot
# Author: warn
# Date: 2017/3/25

import pycuda.autoinit
import pycuda.driver as drv
import numpy as np

from pycuda.compiler import SourceModule

MATRIX_SIZE = 20

kernel_code_template = """
__global__ void multiply_them(float *dest, float *a, float *b)
{
  int tx = threadIdx.x;
  int ty = threadIdx.y;

  int bx = blockIdx.x;
  int by = blockIdx.y;

  int row = by*blockDim.y + ty;
  int col = bx*blockDim.x + tx;
  
  int n = %(MATRIX_SIZE)s;
  if(row < n && col < n){
    int i = row * n + col;
    dest[i] = a[i] * b[i];
  }
}
"""

kernel_code = kernel_code_template % {
    'MATRIX_SIZE': MATRIX_SIZE
    }
mod = SourceModule(kernel_code)

multiply_them = mod.get_function("multiply_them")

if __name__ == '__main__':
    from pycuda import gpuarray

    a = np.random.randn(MATRIX_SIZE, MATRIX_SIZE).astype(np.float32)
    b = np.random.randn(MATRIX_SIZE, MATRIX_SIZE).astype(np.float32)

    a_gpu = gpuarray.to_gpu(a)
    b_gpu = gpuarray.to_gpu(b)

    c_gpu = gpuarray.empty((MATRIX_SIZE, MATRIX_SIZE), np.float32)

    multiply_them(c_gpu, a_gpu, b_gpu,
                  block=(MATRIX_SIZE, MATRIX_SIZE, 1), grid=(1, 1))

    multiply_them(drv.Out(np.zeros_like(a, dtype=np.float32)), drv.In(a), drv.In(b),
                  block=(MATRIX_SIZE, MATRIX_SIZE, 1), grid=(1, 1))

    print(c_gpu.get() - a * b)