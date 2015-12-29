#!/usr/bin/python
# -*- coding: utf-8 -*-

# File name: data_analysis
# Author: warn
# Date: 23/12/2015 18:54

import numpy
import statsmodels.tsa.stattools as ts
import pandas as pd
from pandas.tseries.offsets import BDay
from scipy import stats

import get_stock_price


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

        self.close_list = list(reversed(self.close_list))

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
            test_list = self.close_list

        x = numpy.array(test_list)
        result = ts.adfuller(x)
        return result

    def get_pvalue(self, test_list=None):
        if not test_list:
            if not self.close_list:
                self.load_close_data()
            test_list = self.close_list

        x = numpy.array(test_list)
        print numpy.corrcoef(x[:-1], x[1:])[0][1]
        result = stats.ttest_ind(x[:-1], x[1:])
        # print len(test_list)
        for i in test_list:
            print i
        # print test_list
        return result


if __name__ == "__main__":
    code = '0001.HK'
    get_stock_price.get_price_data(code, end_date="2015-03-31", start_date="2015-01-04")
    test = DataAnalysis(r"./data/%s.csv" % code)
    test.load_close_data()
    # print test.close_list
    # str1 = ''
    date_period = 90
    print test.get_pvalue()
    print test.get_adfvalue()

    # date = pd.datetime(2015, 1, 1)
    # for i in range(len(test.close_list) - date_period):
    #     test_list = list(reversed(test.close_list))[i:(i + date_period)]
    #     date += BDay(1)
    #     # for i in test_list:
    #     #     str1 = "%s,%s" % (str1, i)
    #
    #     print date, test.get_adfvalue(test_list)
