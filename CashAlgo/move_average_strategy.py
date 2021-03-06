#!/usr/bin/python
# -*- coding: utf-8 -*-

# File name: mean_reversion_strategy1
# Author: warn
# Date: 25/12/2015 20:49

import math
import urllib
import urllib2

import cashAlgoAPI
import numpy
import talib


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
        self.move_average_day = 0

        # the close price of last days
        self.close_price = None

        # usually 2, the confidential factor.
        self.factor = None

        # How many total capital we have in summary
        self.total_capital = None

        # How many capital we have
        self.current_capital = None

        # The volume augment factor
        self.volume_factor = None

        # the value of every day's new factor.
        self.mean_average = None
        self.standard_dev = None

    # Initialize Strategy
    def init(self):

        # Read Parameters
        if self.config.has_option("Strategy", "MeanAverage"):
            self.move_average_day = int(self.config.get("Strategy", "MeanAverage"))

        # self.end_date = self.config.get("MarketData", "EndDate").replace("-", "")
        self.factor = float(self.config.get("Strategy", "Factor"))
        self.volume_factor = float(self.config.get("Strategy", "VolumeFactor"))
        self.current_capital = self.total_capital = float(self.config.get("Risk", "InitialCapital"))
        product_code = self.config.get("MarketData", "ProductCode_1")

        self.cnt = 0
        self.last_price = None
        self.last_date = None
        self.buy_volume = 0

        # Get the past price of this stock.
        self.close_price = self.get_price_data(product_code)
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

            if self.last_price:
                self.close_price.pop(0)
                self.close_price.append(self.last_price)

            self.mean_average = talib.MA(numpy.array(self.close_price), self.move_average_day)[-1]
            self.standard_dev = talib.STDDEV(numpy.array(self.close_price), self.move_average_day)[-1]

        # in case some bad value
        if md.lastPrice < self.mean_average / 10:
            md.lastPrice *= 100

        rsi6 = talib.RSI(numpy.array(self.close_price + [md.lastPrice]), timeperiod=6)[-1]
        rsi9 = talib.RSI(numpy.array(self.close_price + [md.lastPrice]), timeperiod=9)[-1]
        rsi14 = talib.RSI(numpy.array(self.close_price + [md.lastPrice]), timeperiod=15)[-1]
        rsix = talib.RSI(numpy.array(self.close_price + [md.lastPrice]), timeperiod=self.move_average_day)[-1]

        if md.lastPrice + self.factor * self.standard_dev < self.mean_average:

            if rsix < 50:
                print "Buying point appear rsi6: %s, rsi9: %s, rsi14: %s, rsi%s: %s" % (rsi6, rsi9, rsi14,
                                                                                        self.move_average_day, rsix)

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
                # self.current_capital -= int(volume) * md.askPrice1
                # print "Buy: %s %s" % (volume, self.total_capital)

        if int(10 * md.lastPrice) >= int(self.mean_average * 10):
            if self.buy_volume:
                print "Selling point appear rsi6: %s, rsi9: %s, rsi14: %s, rsi%s: %s" % (rsi6, rsi9, rsi14,
                                                                                         self.move_average_day, rsix)
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

    def get_price_data(self, code, start_date="2014-08-27", end_date="2014-12-31"):
        code = '%s.HK' % code[1:]
        time_info = [("s", code)]
        data = start_date.split('-')
        time_info.append(("one_int", "%02d" % (int(data[1]) - 1)))
        time_info.append(("two_int", data[2]))
        time_info.append(("sum_int", data[0]))

        data = end_date.split('-')
        time_info.append(("input_str", "%02d" % (int(data[1]) - 1)))
        time_info.append(("e", data[2]))
        time_info.append(("f", data[0]))

        time_info.append(("g", "input_str"))
        time_info.append(("ignore", ".csv"))

        price_info = self.get(self.DATA_URL, time_info).split('\n')[1:-1]
        price_list = [float(i.split(',')[4]) for i in price_info]
        price_list = list(reversed(price_list))
        return price_list
