#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Project: PythonTest
# File name: util
# Author: Mark Wang
# Date: 28/6/2016

import csv


def get_hmse_from_csv(csv_file):
    hmse = 0.0
    line_num = 0
    with open(csv_file) as file:
        reader = csv.DictReader(file)
        for row in reader:
            origin = float(row['origin'])
            predict = float(row['predict'])
            hmse += (origin / predict - 1) ** 2
            line_num += 1

    if line_num > 1:
        hmse /= line_num
    return hmse


def get_me_from_csv(csv_file):
    me = 0.0
    line_num = 0
    with open(csv_file) as file:
        reader = csv.DictReader(file)
        for row in reader:
            origin = float(row['origin'])
            predict = float(row['predict'])
            me += -origin + predict
            line_num += 1

    if line_num > 1:
        me /= line_num
    return me


def get_avg_from_csv(csv_file):
    avg = 0.0
    line_num = 0
    with open(csv_file) as file:
        reader = csv.DictReader(file)
        for row in reader:
            origin = float(row['origin'])
            avg += origin
            line_num += 1

    if line_num > 1:
        avg /= line_num
    return avg
