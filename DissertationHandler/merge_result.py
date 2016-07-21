#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Project: PythonTest
# File name: merge_result
# Author: Mark Wang
# Date: 30/6/2016

import csv
import os
import shutil

output_path = '/Users/warn/Documents/Projects/stock_price/adj_close/output_1_2_2013_2016/'
source_path = '/Users/warn/PycharmProjects/Dissertation/output'

unused_set = {'0845.HK', '0872.HK', '1181.HK', '1230.HK', '1314.HK', '3777.HK', '8050.HK'}


def format_original_file(file_path):
    stock_list = []
    with open(file_path) as f:
        reader = csv.DictReader(f)
        for line in reader:
            if line['stock'] not in unused_set:
                stock_list.append(line)

    return stock_list


for folder in os.listdir(source_path):
    algorithm_path = os.path.join(source_path, folder)
    if os.path.isdir(algorithm_path):
        for symbol in os.listdir(algorithm_path):
            symbol_path = os.path.join(algorithm_path, symbol)
            if os.path.isdir(symbol_path):
                try:
                    shutil.copytree(symbol_path, os.path.join(output_path, folder, symbol))
                except OSError, e:
                    print e
        target_path = os.path.join(output_path, folder, 'stock_info.csv')
        origin_file = open(os.path.join(algorithm_path, 'stock_info.csv'))
        reader = csv.DictReader(origin_file)
        stock_list = format_original_file(target_path)
        for line in reader:
            stock_list.append(line)

        stock_list.sort(key=lambda x: x['stock'])

        with open(target_path, 'w') as f:
            writer = csv.DictWriter(f, fieldnames=reader.fieldnames)
            writer.writeheader()
            for line in stock_list:
                writer.writerow(line)

        origin_file.close()
