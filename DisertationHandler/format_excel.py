#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Project: PythonTest
# File name: format_excel
# Author: Mark Wang
# Date: 7/7/2016

import csv
import os

import openpyxl

folder_path = '/Users/warn/Documents/Projects/stock_price/adj_close/output_1_2_2013_2016/'

already_formatted = {'0033.HK', '0069.HK', '0076.HK', '0078.HK', '0083.HK', '0101.HK', '0116.HK'}


def format_excel(path):
    file_path = os.path.join(folder_path, 'all_info.xlsx')

    wb = openpyxl.load_workbook(file_path)

    for sheet_name in wb.get_sheet_names():
        if sheet_name in {'CDC', 'MAPE'}:
            continue

        ws = wb.get_sheet_by_name(sheet_name)

        for row in ws.rows[1:]:
            if str(row[0].value) in already_formatted:
                continue
            row[2].value /= 100
            row[5].value /= 100

    wb.save(file_path)


def format_csv(path):
    for file_path, dirs, file_list in os.walk(path):
        if 'stock_info.csv' not in file_list:
            continue

        csv_path = os.path.join(file_path, 'stock_info.csv')
        stock_list = []
        headers = None

        with open(csv_path) as f:
            reader = csv.DictReader(f)
            headers = reader.fieldnames
            for line in reader:
                if line['stock'] not in already_formatted:
                    line['CDC'] = float(line['CDC']) / 100
                    line['MAPE'] = float(line['MAPE']) / 100
                stock_list.append(line)

        with open(csv_path, 'w') as f:
            writer = csv.DictWriter(f, headers)
            writer.writeheader()
            writer.writerows(stock_list)


if __name__ == '__main__':
    format_csv(folder_path)
