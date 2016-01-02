#!/usr/bin/python
# -*- coding: utf-8 -*-

# File name: lag
# Author: warn
# Date: 26/12/2015 12:00

import math
import numpy
from scipy import linalg


def lag(x, n):
    result = []
    len_x = len(x)
    for i in range(n):
        result.append(0)

    for i in range(len_x - n):
        result.append(x[i])

    return result


def ols(y, x):
    q, r = linalg.qr(x, mode='economic')
    xpxi = numpy.linalg.lstsq(numpy.dot(r.transpose(), r), numpy.eye(x.size / len(x)))[0]
    # print xpxi
    return numpy.dot(xpxi, numpy.dot(x.transpose(), y))


def half_life(price_series):
    ylag = []
    len_x = len(price_series)
    for i in range(1):
        ylag.append(0)

    for i in range(len_x - 1):
        ylag.append(price_series[i])
    martix_y = numpy.array(price_series)
    matrix_ylag = numpy.array(ylag)
    delta_y = martix_y - matrix_ylag
    delta_y = delta_y.reshape([len(delta_y), 1])[1:]
    matrix_ylag = matrix_ylag.reshape([len(matrix_ylag), 1])[1:]
    x = []
    for i in matrix_ylag:
        x.append([i[0], 1])

    matrix_x = numpy.array(x)
    q, r = linalg.qr(matrix_x, mode='economic')
    xpxi = numpy.linalg.lstsq(numpy.dot(r.transpose(), r), numpy.eye(matrix_x.size / len(matrix_x)))[0]
    # print xpxi
    ols_beta = numpy.dot(xpxi, numpy.dot(matrix_x.transpose(), delta_y))
    hl = -math.log(2) / ols_beta[0]

    return hl[0]

if __name__ == "__main__":
    y = "31.2,31.3,31.15,31.15,31.1,31.6,31.35,31.2,31.1,30.95,31.35,31.7,31.6,31.75,31.75,31.75,31.95,32.15,31.8,31.8".split(',')
    print half_life([float(i) for i in y])
