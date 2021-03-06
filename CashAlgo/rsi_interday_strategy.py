#!/usr/bin/python
# -*- coding: utf-8 -*-

# File name: rsi_interday_strategy
# Author: warn
# Date: 27/12/2015 15:59

import urllib
import urllib2

import cashAlgoAPI
import numpy
import pandas as pd
import talib
from pandas.tseries.offsets import BDay


class Strategy:
    long_flag = False
    short_flag = False

    def __init__(self):
        self.close_data = []
        self.cnt = 0
        self.last_date = None
        self.rsi_period = 14
        self.hold_volume = 0
        self.total_capital = 0
        self.current_capital = 0
        self.volume_factor = 1.1
        self.last_price = None

    def init(self):
        self.cnt = 0
        self.hold_volume = 0

        if self.config.has_option("Strategy", "MaxDataNumber"):
            data_number = int(self.config.get("Strategy", "MaxDataNumber"))
        else:
            data_number = 20
        if self.config.has_option("Strategy", "RsiPeriod"):
            self.rsi_period = int(self.config.get("Strategy", "RsiPeriod"))
        if self.config.has_option("Strategy", "VolumeFactor"):
            self.volume_factor = int(self.config.get("Strategy", "VolumeFactor"))

        self.current_capital = self.total_capital = float(self.config.get("Risk", "InitialCapital"))
        product_code = self.config.get("MarketData", "ProductCode_1")
        self.close_data = self.get_price_data(product_code, days=max(data_number, self.rsi_period))

    def onMarketDataUpdate(self, market, code, md):

        # The following time is not allowed to trade. Only trade from 9:30 am to 12:00 am, and from 13:00 to 16:00
        time_info = md.timestamp.split('_')
        if not (int(time_info[1][:2]) in (range(10, 12) + range(13, 16)) or
                    (time_info[1][:2] == '09' and int(time_info[1][2:]) >= 3000) or
                        time_info[1][:4] == '1600'):
            return

        # Open price clear all the data
        if self.last_date != time_info[0]:
            self.last_date = time_info[0]

            if self.last_price:
                self.close_data.pop(0)
                self.close_data.append(self.last_price)

            rsi_result = talib.RSI(numpy.array(self.close_data), timeperiod=self.rsi_period)[-1]
            if rsi_result < 30 and not self.long_flag:
                self.long_flag = True
                self.short_flag = False
            elif self.long_flag and 70 > rsi_result >= 30:
                self.long_flag = False
                volume = self.total_capital * 0.1 / md.lastPrice
                if md.lastPrice * volume > self.current_capital >= md.lastPrice:
                    volume = self.current_capital / md.lastPrice

                if volume * md.lastPrice <= self.current_capital:
                    self.long_security(md.timestamp, code, md.askPrice1, volume)

            elif self.long_flag and rsi_result >= 70:
                self.long_flag = False

            elif self.hold_volume:
                if rsi_result > 70 and not self.short_flag:
                    self.short_flag = True
                elif self.short_flag and 70 >= rsi_result > 30:
                    self.short_flag = False
                    self.short_security(md.timestamp, code, md.lastPrice)

    def long_security(self, timestamp, code, price, volume):
        order = cashAlgoAPI.Order(timestamp, 'SEHK', code, str(self.cnt), price, int(volume),
                                  "open", 1, "insert", "market_order", "today")
        self.mgr.insertOrder(order)
        self.cnt += 1
        self.hold_volume += int(volume)
        self.current_capital -= int(volume) * price

    def short_security(self, timestamp, code, price):
        order = cashAlgoAPI.Order(timestamp, 'SEHK', code, str(self.cnt), price, self.hold_volume,
                                  "open", 1, "insert", "market_order", "today")
        self.mgr.insertOrder(order)
        self.cnt += 1
        self.current_capital += self.hold_volume * price
        self.total_capital = self.current_capital
        self.hold_volume = 0

    def onOHLCFeed(self, of):
        md = cashAlgoAPI.MarketData([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
        md.timestamp = of.timestamp
        md.market = of.market
        md.productCode = str(of.productCode)
        md.lastPrice = of.close
        md.askPrice1 = of.close
        md.bidPrice1 = of.close
        md.lastVolume = of.volume

        self.onMarketDataUpdate(of.market, of.productCode, md)

    # Process Order
    def onOrderFeed(self, of):
        pass

    # Process Trade
    def onTradeFeed(self, tf):
        # print "Trade feed: %s price: %s, timestamp: %s volume: %s" % (tf.buySell, tf.price, tf.timestamp, tf.volume)
        pass

    # Process Position
    def onPortfolioFeed(self, portfolioFeed):
        pass

    # Process PnL
    def onPnlperffeed(self, pf):
        # print "dailyPnL: %s" % pf.dailyPnL
        pass

    @staticmethod
    def get(url, data=None):
        if data is not None:
            url_values = urllib.urlencode(data)
            url = "%s?%s" % (url, url_values)
        req = urllib2.Request(url)
        response = urllib2.urlopen(req)
        content = response.read()
        return content

    def get_price_data(self, code, days=90):
        end_date = pd.datetime(2015, 1, 1)
        start_date = end_date - BDay(days)
        code = '%s.HK' % code[1:]
        time_info = [("s", code),
                     ("one_int", "%02d" % (start_date.month - 1)),
                     ("two_int", str(start_date.day)),
                     ("sum_int", str(start_date.year)),
                     ("input_str", "%02d" % (end_date.month - 1)),
                     ("e", str(end_date.day)),
                     ("f", str(end_date.year)),
                     ("g", "input_str"),
                     ("ignore", ".csv")]

        price_info = self.get(self.DATA_URL, time_info).split('\n')[1:-1]
        price_list = [float(i.split(',')[4]) for i in price_info]
        price_list = list(reversed(price_list))
        return price_list
