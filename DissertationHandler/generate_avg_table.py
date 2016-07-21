#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Project: PythonTest
# File name: generate_avg_table
# Author: Mark Wang
# Date: 28/6/2016

import openpyxl

table_latex = r"""\begin{table}[h]
	\centering
	\begin{tabular}{|l|l|l|l|}
		\hline
		\textbf{Stock Symbol} & \textbf{Average Price (HKD)} & \textbf{Stock Symbol} & \textbf{Average Price (HKD)} \\ \hline
		\textbf{0001.HK}      &       & \textbf{0006.HK}      &       \\ \hline
		\textbf{0002.HK}      &       & \textbf{0007.HK}      &       \\ \hline
		\textbf{0003.HK}      &       & \textbf{0008.HK}      &       \\ \hline
		\textbf{0004.HK}      &       & \textbf{0009.HK}      &       \\ \hline
		\textbf{0005.HK}      &       & \textbf{0010.HK}      &       \\ \hline
	\end{tabular}
	\caption{Average Stock Price from 2014-01-06 to 2015-01-06}
	\label{tb:avg20142015}
\end{table}"""

b = table_latex.split('\n')

xlsx_file = '/Users/warn/PycharmProjects/output_data/output5_2010_2015/all_info.xlsx'

wb = openpyxl.load_workbook(xlsx_file)
ws = wb.active
stock_dict = {}
for row in ws.rows:
    if row[0].value.endswith('.HK'):
        stock_dict[row[0].value] = row[-1].value

for i in range(5, 10):
    c = b[i].split('&')
    c[1] = '{}{}'.format(stock_dict['00{:02d}.HK'.format(i - 4)], c[1])
    c[3] = '{}{}'.format(stock_dict['00{:02d}.HK'.format(i + 1)], c[1])
    b[i] = '&'.join(c)

print '\n'.join(b)
