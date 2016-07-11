#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Project: PythonTest
# File name: get_latex_table
# Author: Mark Wang
# Date: 11/7/2016


import openpyxl


def convert_to_latex_code(xlsx_path):
    wb = openpyxl.load_workbook(xlsx_path, read_only=True)
    for sheet_name in wb.get_sheet_names():
        if sheet_name in ['CDC', 'MAPE']:
            continue

        print sheet_name
        print

        ws = wb.get_sheet_by_name(sheet_name)
        latex_code = r"""\resizebox{\textwidth}{!}{%
\begin{tabular}{lrcrrcrrl}
\hline
\textbf{Symbol} & \textbf{MSE} & \textbf{MAPE} & \textbf{MAD} & \textbf{RMSE} & \textbf{CDC} & \textbf{HMSE} & \textbf{ME} & \textbf{AVG.} \\
\hline
"""
        for row in ws.rows:
            if not row[0].value.endswith('.HK'):
                continue

            row_str = row[0].value

            for cell_index in range(1, 9):
                cell_value = row[cell_index].value
                if cell_index in {1, 3, 4, 6, 7}:
                    if cell_value > 0.05:
                        row_str = "{} & {:.2f}".format(row_str, cell_value)
                    else:
                        row_str = "{} & {:.2e}".format(row_str, cell_value)
                elif cell_index in {2, 5}:
                    row_str = "{} & {:.2f}\\%".format(row_str, cell_value * 100)
                else:
                    row_str = "{} & HK\\$ {:.2f}".format(row_str, cell_value)

            if not latex_code.endswith('\n'):
                latex_code = "{} \\\\ \n{}".format(latex_code, row_str)
            else:
                latex_code = "{}{}".format(latex_code, row_str)

        latex_code = """{} \\\\
\\hline
\\end{{tabular}}%
}}""".format(latex_code)

        print latex_code
        print


if __name__ == "__main__":
    convert_to_latex_code('/Users/warn/Documents/Projects/StockPrice/CurrentResult/output_2013_2015/all_info.xlsx')
