#!/usr/bin/python
# -*- coding: utf-8 -*-

# File name: cyclc_rotation
# Author: warn
# Date: 19/1/2016 20:46


def solution(A, K):
    n = len(A)
    if not n:
        return A
    elif K > n:
        K %= n
    A = A[(n - K):] + A[:(n - K)]
    return A


if __name__ == '__main__':
    print solution([], 42)
