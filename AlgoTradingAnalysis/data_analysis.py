#!/usr/bin/python
# -*- coding: utf-8 -*-

# File name: data_analysis
# Author: warn
# Date: 23/12/2015 18:54

import numpy
import statsmodels.tsa.stattools as ts
import pandas as pd
from pandas.tseries.offsets import BDay


class DataAnalysis:
    data_file_path = ""
    close_list = []

    def __init__(self, data_path=None):
        self.data_file_path = data_path

    def load_close_data(self, data_path=None):
        self.close_list = []
        if data_path is None and self.data_file_path is None:
            return

        elif data_path:
            path = data_path

        else:
            path = self.data_file_path

        f = open(path)
        content = f.read()
        f.close()
        data_list = content.split("\n")[1:]
        for i in data_list:
            if i:
                # print i
                self.close_list.append(float(i.split(",")[4]))

    def load_adj_close_data(self, data_path=None):
        self.close_list = []
        if data_path is None and self.data_file_path is None:
            return

        elif data_path:
            path = data_path

        else:
            path = self.data_file_path

        f = open(path)
        content = f.read()
        f.close()
        data_list = content.split("\n")[1:]
        for i in data_list:
            if i:
                # print i
                self.close_list.append(float(i.split(",")[6]))

    def get_adfvalue(self, test_list=None):
        if not test_list:
            if not self.close_list:
                self.load_close_data()
            test_list = list(reversed(self.close_list))

        x = numpy.array(test_list)
        result = ts.adfuller(x)
        return result


if __name__ == "__main__":
    test = DataAnalysis(r"./data/0066.HK.csv")
    test.load_close_data()
    # print test.close_list
    # str1 = ''
    date_period = 60

    date = pd.datetime(2015, 1, 1)
    for i in range(len(test.close_list) - date_period):
        test_list = list(reversed(test.close_list))[i:(i + date_period)]
        date += BDay(1)
        # for i in test_list:
        #     str1 = "%s,%s" % (str1, i)

        print date, test.get_adfvalue(test_list)
