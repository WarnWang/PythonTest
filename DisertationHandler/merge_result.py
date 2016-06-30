#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Project: PythonTest
# File name: merge_result
# Author: Mark Wang
# Date: 30/6/2016

import csv
import os
import shutil

output_path = '/Users/warn/Documents/Projects/stock_price/SmallAverage'
source_path = '/Users/warn/PycharmProjects/Dissertation/output'

for folder in os.listdir(source_path):
    algorithm_path = os.path.join(source_path, folder)
    if os.path.isdir(algorithm_path):
        for symbol in os.listdir(algorithm_path):
            symbol_path = os.path.join(algorithm_path, symbol)
            if os.path.isdir(symbol_path):
                shutil.copytree(symbol_path, os.path.join(output_path, folder, symbol))
        target_path = os.path.join(output_path, folder, 'stock_info.csv')
        origin_file = open(os.path.join(algorithm_path, 'stock_info.csv'))
        target_file = open(target_path, 'a')
        reader = csv.DictReader(origin_file)
        writer = csv.DictWriter(target_file, fieldnames=reader.fieldnames)
        for line in reader:
            writer.writerow(line)

        origin_file.close()
        target_file.close()
