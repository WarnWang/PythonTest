#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Project: PythonTest
# File name: draw_picture
# Author: Mark Wang
# Date: 28/6/2016

import os

from DisertationHandler.picture_plot.picture_plot import PicturePlot

output_path = '/Users/warn/PycharmProjects/Dissertation/Report/graduate-thesis/Figures/Result/'
data_path = '/Users/warn/PycharmProjects/output_data/'

for path, dirs, files in os.walk(data_path):
    for dir_name in dirs:
        if 'output_3_1_2010_2014' in dir_name:
            xlsx_path = os.path.join(path, dir_name, 'all_info.xlsx')
            save_path = os.path.join(output_path, ''.join(dir_name.split('_')[1:]))
            print save_path
            if os.path.isfile(xlsx_path):
                pic = PicturePlot(xlsx_path=xlsx_path, save_path=save_path)
                if not os.path.isdir(save_path):
                    os.makedirs(save_path)
                pic.get_picture()
