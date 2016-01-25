#!/usr/bin/python
# -*- coding: utf-8 -*-

# File name: ma_rsi_strategy
# Author: warn
# Date: 29/12/2015 13:32

import urllib
import urllib2
import math

import numpy
import talib
import pandas as pd
from pandas.tseries.offsets import BDay

import cashAlgoAPI


class Strategy:
    # self.mgr: order manager
    # self.config: configuration reader from parameter panel

    # used to get data from finance yahoo
    DATA_URL = "http://real-chart.finance.yahoo.com/table.csv"

    def __init__(self):

        # how many orders execute
        self.cnt = 0

        # Remember the last price of last trading
        self.last_price = None

        # Used to remark whether this market data is an open date or not.
        self.last_date = None

        # how many volume stocks we have bought
        self.buy_volume = 0

        # the days used to calculate the move average
        self.move_average_day = 14

        # the close price of last days
        self.close_price = []
        # the close price of last days for MACD
        self.close_price_MACD = []

        # usually 2, the confidential factor.
        self.std_factor = 2

        # How many total capital we have in summary
        self.total_capital = None

        # How many capital we have
        self.current_capital = None

        # The volume augment factor
        self.volume_factor = 1.0

        # the value of every day's new factor.
        self.mean_average = 0
        self.standard_dev = 0

        self.rsi_period = 6
        self.rsi_buy_bound = 50
        self.rsi_sell_bound = 70

        self.macd_fast_period = 12
        self.macd_slow_period = 26
        self.macd_signal_period = 9

    # Initialize Strategy
    def init(self):

        # Read Parameters
        if self.config.has_option("Strategy", "MeanAveragePeriod"):
            self.move_average_day = int(self.config.get("Strategy", "MeanAveragePeriod"))
        if self.config.has_option("Strategy", "StdFactor"):
            self.std_factor = float(self.config.get("Strategy", "StdFactor"))
        if self.config.has_option("Strategy", "VolumeFactor"):
            self.volume_factor = float(self.config.get("Strategy", "VolumeFactor"))
        if self.config.has_option("Strategy", "RSIPeriod"):
            self.rsi_period = int(self.config.get("Strategy", "RSIPeriod"))

        if self.config.has_option("Strategy", "RSIBuyBound"):
            self.rsi_buy_bound = int(self.config.get("Strategy", "RSIBuyBound"))
        if self.config.has_option("Strategy", "RSISellBound"):
            self.rsi_sell_bound = int(self.config.get("Strategy", "RSISellBound"))

        if self.config.has_option("Strategy", "MACDFastPeriod"):
            self.macd_fast_period = int(self.config.get("Strategy", "MACDFastPeriod"))
        if self.config.has_option("Strategy", "MACDSlowPeriod"):
            self.macd_slow_period = int(self.config.get("Strategy", "MACDSlowPeriod"))
        if self.config.has_option("Strategy", "MACDSignalPeriod"):
            self.macd_signal_period = int(self.config.get("Strategy", "MACDSignalPeriod"))

        self.current_capital = self.total_capital = float(self.config.get("Risk", "InitialCapital"))
        product_code = self.config.get("MarketData", "ProductCode_1")

        self.cnt = 0
        self.last_price = None
        self.last_date = None
        self.buy_volume = 0


        # Get the past price of this stock.
        # self.close_price = self.get_price_data(product_code, end_date=self.config.get("MarketData", "BeginDate"))
        # print self.close_price
        # self.close_price = [float(i) for i in self.config.get("Strategy", "ClosePrice").split(',')]

    # Process Market Data. Please use onOHLCFeed() in OHLC mode
    def onMarketDataUpdate(self, market, code, md):

        # The following time is not allowed to trade. Only trade from 9:30 am to 12:00 am, and from 13:00 to 16:00
        time_info = md.timestamp.split('_')
        if int(time_info[1][:4]) not in (range(930, 1201) + range(1300, 1601)):
            return

        # For open price record last day close price
        if time_info[0] != self.last_date:
            self.last_date = time_info[0]

            if len(self.close_price) > max(self.rsi_period, self.move_average_day) + 1:
                self.close_price.pop(0)
            if len(self.close_price_MACD) > max(self.macd_slow_period, self.macd_signal_period,
                                                self.macd_fast_period) + 1:
                self.close_price_MACD.pop(0)
                # print self.close_price_MACD

            # print self.close_price

            if self.last_price:
                # print 'date: %s\t%s' % (md.timestamp, self.last_price)
                self.close_price.append(self.last_price)
                self.close_price_MACD.append(self.last_price)

            if len(self.close_price) < max(self.rsi_period, self.move_average_day):
                self.last_price = md.lastPrice
                return

            self.mean_average = talib.MA(numpy.array(self.close_price), self.move_average_day)[-1]
            self.standard_dev = talib.STDDEV(numpy.array(self.close_price), self.move_average_day)[-1]

        if len(self.close_price) < max(self.rsi_period, self.move_average_day):
            self.last_price = md.lastPrice
            return

        # rsi6 = talib.RSI(numpy.array(self.close_price + [md.lastPrice]), timeperiod=6)[-1]
        # rsi9 = talib.RSI(numpy.array(self.close_price + [md.lastPrice]), timeperiod=9)[-1]
        # rsi14 = talib.RSI(numpy.array(self.close_price + [md.lastPrice]), timeperiod=15)[-1]
        rsix = talib.RSI(numpy.array(self.close_price + [md.lastPrice]), timeperiod=self.rsi_period)[-1]
        macd, macdsignal, macdhist = talib.MACD(numpy.array(self.close_price_MACD), fastperiod=self.macd_fast_period,
                                                slowperiod=self.macd_slow_period, signalperiod=self.macd_signal_period)
        macdDiff1 = macd[-1]
        macdDiff2 = macd[-1] - macdsignal[-1]

        onSig = 0

        if md.lastPrice + self.std_factor * self.standard_dev < self.mean_average and rsix < self.rsi_buy_bound and macdDiff1 > -0.25:
            # if rsix < 50:
            # print "Buying point appear rsi%s: %s;  macdDiff1 = %s; macdDiff2 %s" % (self.rsi_period, rsix, macdDiff1, macdDiff2)
            # Increase the buying volume so that we will buy more at second time.
            volume0 = int(self.total_capital / 10 / md.lastPrice)
            n = round(math.log(1 - self.buy_volume / volume0 * (1 - self.volume_factor), self.volume_factor))
            volume = volume0 * self.volume_factor ** (n + 1)
            if md.lastPrice <= self.current_capital < volume * md.lastPrice:
                volume = self.current_capital / md.lastPrice

            if self.current_capital > volume * md.lastPrice:
                order = cashAlgoAPI.Order(md.timestamp, 'SEHK', code, str(self.cnt), md.askPrice1, int(volume),
                                          "open", 1, "insert", "market_order", "today")

                self.mgr.insertOrder(order)
                self.cnt += 1
                self.buy_volume += int(volume)
                onSig = 1
                # self.current_capital -= int(volume) * md.askPrice1
                # print "Buy: %s %s" % (volume, self.total_capital)

        if macdDiff1 > -0 and macdDiff2 > -0.2:
            # if rsix < 50:
            # print "Buying point appear rsi%s: %s;  macdDiff1 = %s; macdDiff2 %s" % (self.rsi_period, rsix, macdDiff1, macdDiff2)
            # Increase the buying volume so that we will buy more at second time.
            if onSig == 1:
                print "also bought"
            volume0 = int(self.total_capital / 10 / md.lastPrice)
            n = round(math.log(1 - self.buy_volume / volume0 * (1 - self.volume_factor), self.volume_factor))
            volume = volume0 * self.volume_factor ** (n + 1)
            if md.lastPrice <= self.current_capital < volume * md.lastPrice:
                volume = self.current_capital / md.lastPrice

            if self.current_capital > volume * md.lastPrice:
                order = cashAlgoAPI.Order(md.timestamp, 'SEHK', code, str(self.cnt), md.askPrice1, int(volume),
                                          "open", 1, "insert", "market_order", "today")

                self.mgr.insertOrder(order)
                self.cnt += 1
                self.buy_volume += int(volume)
                onSig = 1
                # self.current_capital -= int(volume) * md.askPrice1
                # print "Buy: %s %s" % (volume, self.total_capital)

        if int(10 * md.lastPrice) >= int(
                        self.mean_average * 10) and self.buy_volume and rsix > self.rsi_sell_bound and onSig == 0:
            # print "Selling point appear rsi%s: %s" % (self.rsi_period, rsix)
            order = cashAlgoAPI.Order(md.timestamp, 'SEHK', code, str(self.cnt), md.bidPrice1, self.buy_volume,
                                      "open", 2, "insert", "market_order", "today")

            self.mgr.insertOrder(order)
            self.cnt += 1
            # self.current_capital += self.buy_volume * md.bidPrice1
            # self.total_capital = self.current_capital
            # print "Sell: %s %s" % (self.buy_volume, self.total_capital)
            self.buy_volume = 0

        if int(10 * md.lastPrice) >= int(self.mean_average * 10) and self.buy_volume and (
                        macdDiff1 < 0.2 or macdDiff2 < 0) and onSig == 0:
            # print "Selling point appear macd: macdDiff1 = %s; macdDiff2 %s" % (macdDiff1, macdDiff2)
            order = cashAlgoAPI.Order(md.timestamp, 'SEHK', code, str(self.cnt), md.bidPrice1, self.buy_volume,
                                      "open", 2, "insert", "market_order", "today")

            self.mgr.insertOrder(order)
            self.cnt += 1
            # self.current_capital += self.buy_volume * md.bidPrice1
            # self.total_capital = self.current_capital
            # print "Sell: %s %s" % (self.buy_volume, self.total_capital)
            self.buy_volume = 0

        self.last_price = md.lastPrice

    # Used in OHLC mode.
    def onOHLCFeed(self, of):
        # print "feed price of %s is %s" % (of.productCode, of.close)
        md = cashAlgoAPI.MarketData([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
        md.timestamp = of.timestamp
        md.market = of.market
        md.productCode = str(of.productCode)
        md.lastPrice = of.close
        md.askPrice1 = of.close
        md.bidPrice1 = of.close
        md.lastVolume = 1

        self.onMarketDataUpdate(of.market, of.productCode, md)

    # Process Order
    def onOrderFeed(self, of):
        pass

    # Process Trade
    def onTradeFeed(self, tf):
        # print "buySell: %s, price: %s, timestame: %s, volume: %s, volumeFilled: %s" % (tf.buySell, tf.price,
        #                                                                                tf.timestamp, tf.volume,
        #                                                                                tf.volumeFilled)
        # # print "Trade feed: %s price: %s, timestamp: %s volume: %s" % (tf.buySell, tf.price, tf.timestamp, tf.volume)
        if tf.buySell == 1:
            self.current_capital -= tf.volumeFilled * tf.price
        else:
            self.current_capital += tf.volumeFilled * tf.price
            self.total_capital = self.current_capital

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

    def get_price_data(self, code, end_date=None, days=90):
        if end_date is None:
            end_date = pd.datetime(2014, 12, 31)
        else:
            time_info = end_date.split('-')
            end_date = pd.datetime(int(time_info[0]), int(time_info[1]), int(time_info[2])) - BDay(1)
        start_date = end_date - BDay(days)
        code = '%s.HK' % code[1:]
        time_info = [("s", code),
                     ("a", "%02d" % (start_date.month - 1)),
                     ("b", str(start_date.day)),
                     ("c", str(start_date.year)),
                     ("d", "%02d" % (end_date.month - 1)),
                     ("e", str(end_date.day)),
                     ("f", str(end_date.year)),
                     ("g", "d"),
                     ("ignore", ".csv")]

        price_info = self.get(self.DATA_URL, time_info).split('\n')[1:-1]
        price_list = [float(i.split(',')[4]) for i in price_info]
        price_list = list(reversed(price_list))
        return price_list
