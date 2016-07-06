#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Project: PythonTest
# File name: draw_picture
# Author: Mark Wang
# Date: 28/6/2016

import os
import re

from DisertationHandler.picture_plot.picture_plot import PicturePlot

output_path = '/Users/warn/Documents/Projects/Dissertation/graduate-thesis/Figures/AdjClose'
data_path = '/Users/warn/Documents/Projects/stock_price/adj_close'

for path, dirs, files in os.walk(data_path):
    for dir_name in dirs:
        xlsx_path = os.path.join(path, dir_name, 'all_info.xlsx')
        if os.path.isfile(xlsx_path):
            years = re.findall(r'\d{4}', dir_name)
            save_path = os.path.join(output_path, ''.join(years))
            print save_path
            if os.path.isfile(xlsx_path):
                pic = PicturePlot(xlsx_path=xlsx_path, save_path=save_path)
                if not os.path.isdir(save_path):
                    os.makedirs(save_path)
                pic.get_picture()
