#!/usr/bin/python
# -*- coding: utf-8 -*-

# File name: final_strategy
# Author: warn
# Date: 26/12/2015 20:17

import urllib
import urllib2
import math

import numpy
import talib
import pandas as pd
from pandas.tseries.offsets import BDay

import cashAlgoAPI

TREND = 'trend'
MEAN = 'mean'


class Strategy:
    # self.mgr: order manager
    # self.config: configuration reader from parameter panel

    # used to get data from finance yahoo
    DATA_URL = "http://real-chart.finance.yahoo.com/table.csv"

    def __init__(self):

        # how many orders execute
        self.cnt = 0

        # To remark some system parameters
        # the close price of last days
        self.close_price = None

        # Remember the last price of last trading
        self.last_price = None

        # Used to remark whether this market data is an open date or not.
        self.last_date = None

        ###############################################################################################
        # The following parameters are used for MA strategy
        # Used to store every days moving average
        self.move_average = None

        # the days used to calculate the move average
        self.move_average_period = 0

        # the standard deviation value of every day
        self.standard_deviation = None

        # usually 2, the confidential factor.
        self.ma_std_factor = 2
        self.first_buy_factor = 0.1

        ###############################################################################################
        # The following parameters are used for RSI strategy and MACD strategy
        # store the daily rsi value
        self.rsi = None

        # usually 9 for short period 14 for middle period and 22 for long period
        self.rsi_period = 14

        # used for restore macd value
        self.macd = None
        self.macd_fast_period = 12
        self.macd_slow_period = 26
        self.macd_time_signal = 9

        ###############################################################################################
        # The following store some parameters for ADF test values
        self.adf_period = 90

        ###############################################################################################
        # the volume factor determined how many volume argument should be taken into account, used in rsi
        # and MA strategy
        self.volume_factor = 1

        # How many total capital we have in summary
        self.total_capital = {MEAN: 0,
                              TREND: 0}

        # How many capital we have
        self.current_capital = {MEAN: 0,
                                TREND: 0}

        # how many volume stocks we have bought
        self.hold_volume = {MEAN: 0,
                            TREND: 0}

        # how many stocks total we have bought
        self.hold_price = {MEAN: 0,
                           TREND: 0}

    # Initialize Strategy
    def init(self):

        # Read Parameters
        if self.config.has_option("Strategy", "MeanAveragePeriod"):
            self.move_average_period = int(self.config.get("Strategy", "MeanAveragePeriod"))
        if self.config.has_option("Strategy", "MAStdFactor"):
            self.ma_std_factor = float(self.config.get("Strategy", "MAStdFactor"))
        if self.config.has_option("Strategy", "RSIPeriod"):
            self.rsi_period = int(self.config.get("Strategy", "RSIPeriod"))
        if self.config.has_option("Strategy", "MACDFastPeriod"):
            self.macd_fast_period = int(self.config.get("Strategy", "MACDFastPeriod"))
        if self.config.has_option("Strategy", "MACDSlowPeriod"):
            self.macd_slow_period = int(self.config.get("Strategy", "MACDSlowPeriod"))
        if self.config.has_option("Strategy", "MACDTimeSignal"):
            self.macd_time_signal = int(self.config.get("Strategy", "MACDTimeSignal"))
        if self.config.has_option("Strategy", "ADFPeriod"):
            self.adf_period = int(self.config.get("Strategy", "ADFPeriod"))
        if self.config.has_option("Strategy", "VolumeFactor"):
            self.volume_factor = float(self.config.get("Strategy", "VolumeFactor"))

        self.total_capital[TREND] = float(self.config.get("Risk", "InitialCapital"))
        product_code = self.config.get("MarketData", "ProductCode_1")

        # Get the past price of this stock.
        self.close_price = self.get_price_data(product_code, days=max(self.adf_period,
                                                                      self.macd_slow_period,
                                                                      self.rsi_period))
        # self.close_price = [float(i) for i in self.config.get("Strategy", "ClosePrice").split(',')]

    # Process Market Data. Please use onOHLCFeed() in OHLC mode
    def onMarketDataUpdate(self, market, code, md):

        # The following time is not allowed to trade. Only trade from 9:30 am to 12:00 am, and from 13:00 to 16:00
        time_info = md.timestamp.split('_')
        if int(time_info[1][:2]) not in (range(10, 12) + range(13, 16)) or (time_info[1][:2] == '09' and
                                                                                    int(time_info[1][2:]) < 3000):
            return

        # For open price record last day close price
        if time_info[0] != self.last_date:
            self.last_date = time_info[0]

            if self.last_price:
                self.close_price.pop(0)
                self.close_price.append(self.last_price)

        mean_average = talib.MA(numpy.array(self.close_price), self.move_average_period)[-1]
        standard_dev = talib.STDDEV(numpy.array(self.close_price))[-1]

        # in case some bad value
        if md.lastPrice < mean_average / 10:
            md.lastPrice *= 100

        if md.lastPrice + self.ma_std_factor * standard_dev < mean_average:
            volume0 = int(self.total_capital / 10 / md.lastPrice)
            n = round(math.log(1 - self.hold_volume / volume0 * (1 - self.volume_factor), self.volume_factor))
            volume = volume0 * self.volume_factor ** (n + 1)
            if md.lastPrice <= self.current_capital < volume * md.lastPrice:
                volume = self.current_capital / md.lastPrice

            if self.current_capital > volume * md.lastPrice:
                order = cashAlgoAPI.Order(md.timestamp, 'SEHK', code, str(self.cnt), md.askPrice1, volume,
                                          "open", 1, "insert", "market_order", "today")

                self.mgr.insertOrder(order)
                self.cnt += 1
                self.hold_volume += volume
                self.current_capital -= volume * md.askPrice1
                print "Buy: %s %s" % (volume, self.total_capital)

        if int(10 * md.lastPrice) >= int(mean_average * 10) and self.hold_volume:
            order = cashAlgoAPI.Order(md.timestamp, 'SEHK', code, str(self.cnt), md.bidPrice1, self.hold_volume,
                                      "open", 2, "insert", "market_order", "today")

            self.mgr.insertOrder(order)
            self.cnt += 1
            self.current_capital += self.hold_volume * md.bidPrice1
            self.total_capital = self.current_capital
            print "Sell: %s %s" % (self.hold_volume, self.total_capital)
            self.hold_volume = 0

        self.last_price = md.lastPrice

    def short_securities(self, strategy, code, timestamp, price):
        order = cashAlgoAPI.Order(timestamp, 'SEHK', code, str(self.cnt), price, self.hold_volume[strategy],
                                  "open", 2, "insert", "market_order", "today")

        self.mgr.insertOrder(order)
        self.cnt += 1
        sell_capital = self.hold_volume[strategy] * price
        interest = sell_capital - self.hold_price[strategy]
        total_capital = self.total_capital[MEAN] + self.total_capital[TREND] + interest
        current_mean_factor = float(self.total_capital[MEAN]) / (self.total_capital[TREND] + self.total_capital[MEAN])
        self.total_capital[MEAN] = total_capital * current_mean_factor
        self.total_capital[TREND] = total_capital * (1 - current_mean_factor)
        self.current_capital[strategy] += sell_capital
        if self.current_capital[strategy] > self.total_capital[strategy]:
            difference = self.current_capital[strategy] - self.total_capital[strategy]
            other_strategy = MEAN if strategy == TREND else TREND
            self.current_capital[strategy] -= difference
            self.current_capital[other_strategy] += difference

        print "Sell: %s, current total capital is %s" % (self.hold_volume[strategy], self.total_capital)
        self.hold_volume[strategy] = 0
        self.hold_price[strategy] = 0

    def long_securities(self, strategy, code, timestamp, price):
        if strategy == TREND:
            volume = int(self.current_capital[strategy] / price)
        else:
            volume0 = int(self.total_capital[strategy] * self.first_buy_factor / price)
            n = round(math.log(1 - self.buy_volume / volume0 * (1 - self.volume_factor), self.volume_factor))
            volume = int(volume0 * self.volume_factor ** (n + 1))
            if price <= self.current_capital[MEAN] < volume * price:
                volume = self.current_capital[MEAN] / price
            elif self.current_capital[MEAN] < price:
                print "%s, current money is %s, cannot buy" % (timestamp, self.current_capital[MEAN])
                volume = 0

        if volume:
            order = cashAlgoAPI.Order(timestamp, 'SEHK', code, str(self.cnt), price, volume,
                                      "open", 1, "insert", "market_order", "today")

            self.mgr.insertOrder(order)
            self.cnt += 1
            self.current_capital[strategy] -= volume * price
            print "Buy: %s, current total capital is %s" % (volume, self.total_capital)
            self.hold_volume[strategy] += volume
            self.hold_price[strategy] += volume * price

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
        pass
        # print "Trade feed: %s price: %s, timestamp: %s volume: %s" % (tf.buySell, tf.price, tf.timestamp, tf.volume)

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
        end_date = pd.datetime.date(2015, 1, 1)
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
                     ("ignore", ".csv")
                     ]

        price_info = self.get(self.DATA_URL, time_info).split('\n')
        price_list = [float(i.split(',')[4]) for i in price_info]
        price_list = reversed(price_list)
        return price_list
