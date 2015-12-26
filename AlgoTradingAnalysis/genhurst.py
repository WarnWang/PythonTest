#!/usr/bin/python
# -*- coding: utf-8 -*-

# File name: genhurst
# Author: warn
# Date: 24/12/2015 21:24

import numpy


def genhurst(S, q=1, maxT=19):
    s = numpy.array(S)
    s = s.transpose()
