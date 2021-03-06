#!/usr/bin/python
# -*- coding: utf-8 -*-

# File name: data_analysis
# Author: warn
# Date: 23/12/2015 18:54

import numpy
import statsmodels.tsa.stattools as ts
import pickle

from scipy import stats
import talib

import lag


class DataAnalysis:
    data_file_path = ""
    close_list = []
    time_list = []
    high_list = []
    low_list = []

    def __init__(self, data_path=None):
        self.data_file_path = data_path

    def load_close_data(self, data_path=None):
        self.close_list = []
        self.time_list = []
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
                self.time_list.append(i.split(",")[0])

        self.close_list = list(reversed(self.close_list))
        self.time_list = list(reversed(self.time_list))

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

    def get_adfvalue(self):

        result = ts.adfuller(self.close_list)
        return result

    def get_pvalue(self, test_list=None):
        if not test_list:
            if not self.close_list:
                self.load_close_data()
            test_list = self.close_list

        x = numpy.array(test_list)
        print numpy.corrcoef(x[:-1], x[1:])[0][1]
        result = stats.ttest_ind(x[:-1], x[1:])
        for i, j in zip(self.time_list, test_list):
            print "%s\t%s" % (i, j)
        return result

    def load_history_data(self, code):
        f = open(self.data_file_path)
        price_dict = pickle.load(f)
        f.close()
        self.close_list = numpy.array(price_dict[code]['close_price'])
        self.high_list = numpy.array(price_dict[code]['high_price'])
        self.low_list = numpy.array(price_dict[code]['low_price'])

    def get_adx_value(self):
        return talib.ADX(self.high_list, self.low_list, self.close_list, timeperiod=14)

    def get_dmi_plus(self):
        return talib.PLUS_DM(self.high_list, self.low_list, timeperiod=14)

    def get_dmi_minus(self):
        return talib.MINUS_DM(self.high_list, self.low_list, timeperiod=14)

    def get_di_plus(self):
        return talib.PLUS_DI(self.high_list, self.low_list, self.close_list, timeperiod=14)

    def get_di_minus(self):
        return talib.MINUS_DI(self.high_list, self.low_list, self.close_list, timeperiod=14)

    def get_stoch_rsi(self):
        return talib.STOCHRSI(self.close_list, timeperiod=14)

    def get_sma_minus_ma(self):
        return talib.SMA(self.close_list, timeperiod=20) - talib.MA(self.close_list, timeperiod=20)

    def get_tsf(self):
        return talib.TSF(self.close_list)

    def get_ppo(self):
        return talib.PPO(self.close_list, fastperiod=5, slowperiod=35)

    def get_half_life(self):
        return lag.half_life(self.close_list)


def get_all_adf_value():
    stock_list = open('stock_list')
    test = DataAnalysis(r"stock_price_2015_s1.txt")
    adf_value = open('half_life.csv', 'w')
    for i in stock_list:
        test.load_history_data('0%s' % i.strip('\n'))
        adf = test.get_half_life()
        adf_value.write('%s, %s\n' % (i.strip('\n'), adf))

    stock_list.close()
    adf_value.close()


if __name__ == "__main__":
    get_all_adf_value()
