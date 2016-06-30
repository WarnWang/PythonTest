#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Project: PythonTest
# File name: util
# Author: Mark Wang
# Date: 28/6/2016

import csv
import datetime


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


def str2datetime(string):
    return datetime.datetime(year=int(string.split('-')[0]),
                             month=int(string.split('-')[1]),
                             day=int(string.split('-')[2]))


def next_month(date_info):
    month = date_info.month
    if month == 12:
        return datetime.datetime(year=date_info.year + 1, month=1, day=date_info.day)
    else:
        return datetime.datetime(year=date_info.year, month=date_info.month + 1, day=date_info.day)


def get_monthly_mape(file_path, start_date):
    if isinstance(start_date, str):
        start_date = str2datetime(start_date)
    mapes = []
    print file_path
    with open(file_path) as file:
        csv_dict = csv.DictReader(file)
        end_date = next_month(start_date)
        month_data = []
        for line in csv_dict:
            price_date = str2datetime(line['date'])
            if price_date <= start_date:
                continue
            if price_date <= end_date:
                month_data.append((float(line['origin']), float(line['predict'])))
            else:
                mapes.append(sum(map(lambda (o, p): abs(o - p) / o, month_data)) / len(month_data))
                month_data = []
                end_date = next_month(end_date)

        mapes.append(sum(map(lambda (o, p): abs(o - p) / o, month_data)) / len(month_data))

    return mapes
