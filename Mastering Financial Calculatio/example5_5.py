#!/usr/bin/python
# -*- coding: utf-8 -*-

# File name: example5_5
# Author: warn
# Date: 25/1/2016 13:26

ytm = 0.1106
r = 0.1
pv = 95
fv = 100
q = (1 + ytm) ** -1
print fv * q * (r * (1 - q ** 7) / (1 - q) + q ** 6)
