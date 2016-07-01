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


if __name__ == '__main__':
    s = '''0431.HK G CHINA FIN
0377.HK HUAJUN HOLD
1195.HK KINGWELL GROUP
0845.HK GLORIOUS PPT H
1170.HK KINGMAKER
6823.HK HKT-SS
0066.HK MTR CORPORATION
0054.HK HOPEWELL HOLD
0011.HK HANG SENG BANK
0012.HK HENDERSON LAND
0013.HK HUTCHISON
0014.HK HYSAN DEV
0015.HK VANTAGE INT'L
0016.HK SHK PPT
0017.HK NEW WORLD DEV
0018.HK ORIENTAL PRESS
0019.HK SWIRE PACIFIC A
0020.HK WHEELOCK
0021.HK GREAT CHI PPT
0022.HK MEXAN
0023.HK BANK OF E ASIA
0024.HK BURWILL
0025.HK CHEVALIER INT'L
0026.HK CHINA MOTOR BUS
0027.HK GALAXY ENT
0028.HK TIAN AN
0029.HK DYNAMIC HOLD
0030.HK BAN LOONG HOLD
0031.HK CHINA AEROSPACE
0032.HK CROSS-HAR(HOLD)
0700.HK TENCENT
0034.HK KOWLOON DEV
0035.HK FE CONSORT INTL
0068.HK LEE HING
0038.HK FIRST TRACTOR
0039.HK CH BEIDAHUANG
0040.HK GOLD PEAK'''
    f = open('symbol_list.csv', 'w')
    writer = csv.DictWriter(f, fieldnames=['Stock Symbol', 'Company Name'])
    writer.writeheader()
    for line in s.split('\n'):
        word1 = line[:7]
        word2 = line[8:]
        writer.writerow({'Stock Symbol': word1, 'Company Name': word2})
    f.close()
