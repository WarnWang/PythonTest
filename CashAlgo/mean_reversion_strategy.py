#!/usr/bin/python
# -*- coding: utf-8 -*-

# File name: mean_reversion_strategy
# Author: warn
# Date: 24/12/2015 21:00

import cashAlgoAPI
import CardsLib
import CardsILib
import collections

LAST_DATE = "last_date"
CLOSE_PRICE = "close_price"
LOW_PRICE = "low_price"
LAST_LOW_PRICE = "yesterday_low"
MEAN_AVERAGE = "mean_average"
LAST_PRICE = "last_price"


class Strategy:
    # self.mgr: order manager
    # self.config: configuration reader from parameter panel

    def __init__(self):

        # how many orders execute
        self.cnt = 0

        # Daily execute security number
        self.execute_number = None

        # Total Security Number
        self.security_num = None

        # The daily open price of each product
        self.open_price = {}

        # This dict stores the potential stocks can be traded
        self.bog_array = {}

        # stores the low price, yesterday low price of every security
        self.security_info = {}

        # When trade happened, how many stocks need to buy
        self.volume = 100

        # if every day we can earn this factor of money, we will sell all the holding stocks
        self.factor_threshold = None

        # A flag to remark whether the open bid is executed or not, False for not
        self.open_execute = False

    # Initialize Strategy
    def init(self):
        # Read Parameters
        if self.config.has_option("Strategy", "SecNum"):
            self.security_num = int(self.config.get("Strategy", "SecNum"))
        if self.config.has_option("Strategy", "ExeNum"):
            self.execute_number = int(self.config.get("Strategy", "ExeNum"))
        if self.config.has_option("Strategy", "Volume"):
            self.volume = int(self.config.get("Strategy", "Volume"))
        if self.config.has_option("Strategy", "Threshold"):
            self.factor_threshold = float(self.config.get("Strategy", "Threshold"))
        if self.config.has_option("Strategy", "MeanAverage"):
            mean_average_day = int(self.config.get("Strategy", "MeanAverage"))

        self.cnt = 0
        for i in range(1, self.security_num + 1):
            if self.config.has_option("MarketData", "ProductCode_%d" % i):
                product_code = self.config.get("MarketData", "ProductCode_%d" % i)
                self.security_info[product_code] = {LAST_DATE: None,
                                                    LAST_LOW_PRICE: 999999,
                                                    LOW_PRICE: 999999,
                                                    CLOSE_PRICE: 999999,
                                                    LAST_PRICE: 999999,
                                                    MEAN_AVERAGE: CardsILib.MovingAverage(mean_average_day)}
        self.security_num = len(self.security_info)
        if self.execute_number >= self.security_num:
            self.execute_number = self.security_num / 3
            if not self.execute_number:
                self.execute_number += 1
        self.bog_array.clear()
        self.open_price.clear()

    # Process Market Data. Please use onOHLCFeed() in OHLC mode
    def onMarketDataUpdate(self, market, code, md):

        time_info = md.timestamp.split('_')
        if int(time_info[1]) not in (range(93000, 120000) + range(130000, 155959)):
            return

        # For open price
        if time_info[0] != self.security_info[code][LAST_DATE]:
            # print "open price of %s is %s" % (code, md.lastPrice)
            self.open_execute = False
            print "mean reversion price of code %s: %s" % (code, self.security_info[code][MEAN_AVERAGE].price)

            if len(self.open_price) == self.security_num:
                self.open_price.clear()

            self.security_info[code][LAST_DATE] = time_info[0]
            self.security_info[code][LAST_LOW_PRICE] = self.security_info[code][LOW_PRICE]
            self.security_info[code][LOW_PRICE] = md.lastPrice

            # mark how many stocks have been dealt
            self.open_price[code] = md.askPrice1

            # print "yesterday's close price:%f" % self.today_low[code]
            bog_rate = self.open_price[code] - self.security_info[code][LAST_LOW_PRICE]
            # print "open price of %s is %s and its bog rate: %s" % (code, md.lastPrice, bog_rate)

            if bog_rate > 0 and self.open_price[code] > self.security_info[code][MEAN_AVERAGE].price:
                self.bog_array[code] = bog_rate / self.security_info[code][LAST_LOW_PRICE]

        # The open bid strategy
        if len(self.open_price) == self.security_num and not self.open_execute:
            sorted_array = collections.OrderedDict(sorted(self.bog_array.items(), key=lambda t: t[1], reverse=False))
            self.bog_array.clear()

            # print "array %s" % str(sorted_array)
            execute_number = 0
            while execute_number < self.execute_number:
                if sorted_array:
                    buy_code = sorted_array.popitem(True)
                    order = cashAlgoAPI.Order(md.timestamp, 'SEHK', buy_code[0], str(self.cnt),
                                              self.open_price[buy_code[0]], self.volume, "open", 1, "insert",
                                              "market_order", "today")

                    # print "Place an BUY order at %s" % of.timestamp
                    self.mgr.insertOrder(order)
                    self.cnt += 1
                    execute_number += 1
                    self.bog_array[buy_code[0]] = None
                else:
                    break

            self.open_execute = True

        # At the end of everyday sell all the product
        if code in self.bog_array and (time_info[1][:4] == '1559' or
                                               float(md.bidPrice1) >= self.factor_threshold * float(
                                                   self.open_price[code])):
            del self.bog_array[code]
            order = cashAlgoAPI.Order(md.timestamp, market, code, str(self.cnt), md.bidPrice1, self.volume, "open", 2,
                                      "insert", "market_order", "today")
            self.mgr.insertOrder(order)
            self.cnt += 1

        if time_info[1][:4] == '1559':
            self.security_info[code][MEAN_AVERAGE].update(md)

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

        if self.security_info[of.productCode][LOW_PRICE] > of.low:
            self.security_info[of.productCode][LOW_PRICE] = of.low

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
