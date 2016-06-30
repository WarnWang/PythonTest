#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Project: PythonTest
# File name: picture_plot
# Author: Mark Wang
# Date: 28/6/2016

import os

import numpy as np
import openpyxl

from DisertationHandler.util import *
from ForFun.test_char import test_char

sheet_name_dict = {'Artificial_Neural_Network'.lower(): "ANN",
                   'Artificial_Random'.lower(): 'ANN + Random Forest',
                   'Linear_Logistic'.lower(): 'Linear Regression + Logistic Regression',
                   'Linear_Regression'.lower(): 'Linear Regression',
                   'Random_Forest'.lower(): 'Random Forest',
                   'Random_SVM'.lower(): 'Random Forest + SVM'}

short_name_dict = {'Artificial_Neural_Network'.lower(): "ANN",
                   'Artificial_Random'.lower(): 'ANN_RF',
                   'Linear_Logistic'.lower(): 'LR_LR',
                   'Linear_Regression'.lower(): 'LR',
                   'Random_Forest'.lower(): 'RF',
                   'Random_SVM'.lower(): 'RF_SVM'}

picture_list = ['MSE', 'MAPE', 'MAD', 'RMSE', 'CDC', 'HMSE', 'ME']
# picture_list = ['MAPE', 'HMSE']
tick_list = ['0001.HK', '0002.HK', '0003.HK', '0004.HK', '0005.HK', '0006.HK', '0007.HK', '0008.HK',
             '0009.HK',
             '0010.HK']
color_list = ['r', 'b', 'g', 'y', 'orange', 'brown']
algorithm_list = ['ANN', 'Linear Regression', 'Random Forest', 'ANN + Random Forest',
                  'Linear Regression + Logistic Regression', 'Random Forest + SVM']


class PicturePlot(object):
    def __init__(self, xlsx_path, save_path):
        self.wb_path = xlsx_path
        self.save_path = save_path

    def read_data_from_file(self):
        wb = openpyxl.load_workbook(self.wb_path, read_only=True)
        algorithm_info = {}
        for sheet_name in wb.get_sheet_names():
            if sheet_name.lower() not in sheet_name_dict:
                continue

            algorithm = sheet_name_dict[sheet_name.lower()]
            algorithm_info[algorithm] = {}
            ws = wb.get_sheet_by_name(name=sheet_name)
            for row in ws.rows:
                if row[0].value.endswith('.HK'):
                    algorithm_info[algorithm][row[0].value] = {}
                    for i in range(1, len(row)):
                        algorithm_info[algorithm][row[0].value][ws["{}1".format(test_char(i))].value.strip()] = row[
                            i].value

        return algorithm_info

    def get_monthly_data(self, start_date='2014-01-06'):
        import matplotlib.pyplot as plt
        test_path = self.wb_path.split('/')[:-1]
        test_path = os.path.join('/', '/'.join(test_path))
        method_dict = {}
        ticks = range(1, 13)
        for path, dirs, files in os.walk(test_path):
            if "predict_result.csv" in files:
                fig = plt.figure()
                method = path.split('/')[-2]
                symbol = path.split('/')[-1]
                if method not in method_dict:
                    method_dict[method] = np.zeros(12)
                save_path = os.path.join(self.save_path, "{}_{}.png".format(short_name_dict[method.lower()], symbol))
                mapes = get_monthly_mape(os.path.join(path, "predict_result.csv"), start_date=start_date)
                method_dict[method] += mapes
                plt.plot(ticks, mapes)
                plt.ylabel("MAPE (%)")
                plt.grid(True)
                plt.title('Stock {}.HK monthly MAPE method {}'.format(symbol, sheet_name_dict[method.lower()]))
                plt.savefig(save_path)

                plt.close()

        for method in method_dict:
            fig = plt.figure()
            save_path = os.path.join(self.save_path, "{}_AVG_MAPE.png".format(short_name_dict[method.lower()]))
            plt.plot(ticks, method_dict[method] * 10)
            plt.ylabel("MAPE (%)")
            plt.grid(True)
            plt.title('{} 10 stocks monthly MAPE'.format(sheet_name_dict[method.lower()]))
            plt.savefig(save_path)
            plt.close()

    def get_picture(self):
        import matplotlib.pyplot as plt
        info_dict = self.read_data_from_file()
        for i, picture in enumerate(picture_list):
            fig = plt.figure(i)
            list_dict = {}
            new_tick_list = tick_list[:]
            for algorithm in algorithm_list:
                list_dict[algorithm] = []
            for symbol in new_tick_list:
                for algorithm in algorithm_list:
                    # if picture in ['HMSE']:
                    #     list_dict[algorithm].append(np.log10(info_dict[algorithm][symbol][picture]))
                    # elif picture == 'MAPE':
                    #     list_dict[algorithm].append(np.log10(info_dict[algorithm][symbol][picture] / 100))
                    # else:
                    list_dict[algorithm].append(info_dict[algorithm][symbol][picture])

            opacity = 0.4
            bar_width = 0.12
            index = np.arange(len(new_tick_list))

            for i, algorithm in enumerate(algorithm_list):
                plt.bar(index + bar_width * i, list_dict[algorithm], bar_width,
                        alpha=opacity,
                        color=color_list[i],
                        label=algorithm)
            plt.xlabel('Stock Symbol')
            plt.ylabel(picture)
            plt.xticks(index + 3 * bar_width, new_tick_list)
            plt.legend(loc=0)
            file_path = os.path.join(self.save_path, '{}.png'.format(picture))
            size = fig.get_size_inches()
            fig.set_size_inches(size * 1.5, forward=False)
            fig.savefig(file_path)

        for algorithm in info_dict:
            cdc = 0.0
            for symbol in info_dict[algorithm]:
                cdc += info_dict[algorithm][symbol]['CDC']
            print algorithm, cdc / 10
        plt.close()


if __name__ == '__main__':
    test = PicturePlot(xlsx_path='/Users/warn/PycharmProjects/output_data/output4_2012_2016/all_info.xlsx',
                       save_path='/Users/warn/Documents/Projects/Dissertation/graduate-thesis/Figures/Result/20122016')

    # test.get_monthly_data(start_date='2015-01-06')
    test.get_picture()
    # import pprint

    info = test.read_data_from_file()
    # pprint.pprint(info['Random Forest + SVM'], width=150)
    # pprint.pprint(info['Linear Regression + Logistic Regression'], width=150)

    for algorithm in info:
        mape = 0.0
        for stock_symbol in info[algorithm]:
            mape += info[algorithm][stock_symbol]['MAPE']
        print algorithm, mape / 10
