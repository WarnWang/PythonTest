#!/usr/bin/python
# -*- coding: utf-8 -*-

# Project: PythonTest
# File name: evaluation_function
# Author: Mark Wang
# Date: 17/3/2016

import time


def evaluation_function_runtime(evaluate_function, n=100, *args, **kwargs):
    start_time = time.time()
    for i in range(n):
        k = evaluate_function(*args, **kwargs)
    end_time = time.time()

    print "Running time is {}".format((end_time - start_time) / n)
    return k


if __name__ == "__main__":
    from reverse_str import *

    string_input = "abcdedfsefsfasfaasdfaeravaewrewatsdfasd" * 1000
    print evaluation_function_runtime(reverse_tradition_version, 100, string_input)
    print evaluation_function_runtime(reverse_version_1, 100, string_input)
    print evaluation_function_runtime(reverse_version_2, 100, string_input)
    print evaluation_function_runtime(reverse_version_3, 100, string_input)
