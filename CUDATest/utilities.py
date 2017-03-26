#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Project: PythonTest
# File name: utilities
# Author: warn
# Date: 2017/3/25

from timeit import repeat
import threading

import numpy as np


def timefunc(correct, s, func, *args, **kwargs):
    """
    Benchmark *func* and print out its runtime.
    """
    print(s.ljust(20), end=" ")
    # Make sure the function is compiled before we start the benchmark
    res = func(*args, **kwargs)
    if correct is not None:
        assert np.allclose(res, correct), (res, correct)
    # time it
    print('{:>5.0f} ms'.format(min(repeat(lambda: func(*args, **kwargs),
                                          number=5, repeat=2)) * 1000))
    return res
