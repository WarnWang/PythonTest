#!/usr/bin/python
# -*- coding: utf-8 -*-

# File name: mean_reversion_strategy1
# Author: warn
# Date: 25/12/2015 20:49


import cashAlgoAPI
import talib
import numpy


class Strategy:
    # self.mgr: order manager
    # self.config: configuration reader from parameter panel

    def __init__(self):

        # how many orders execute
        self.cnt = 0

        # The daily open price of each product
        self.last_price = None
        self.last_date = None
        self.buy_volume = 0
        self.move_average_day = 0
        self.close_price = None
        # self.end_date = None
        self.factor = None
        self.total_capital = None
        self.current_capital = None

    # Initialize Strategy
    def init(self):
        # Read Parameters
        if self.config.has_option("Strategy", "MeanAverage"):
            self.move_average_day = int(self.config.get("Strategy", "MeanAverage"))

        # self.end_date = self.config.get("MarketData", "EndDate").replace("-", "")
        self.factor = float(self.config.get("Strategy", "Factor"))
        self.current_capital = self.total_capital = float(self.config.get("Risk", "InitialCapital"))

        self.cnt = 0
        self.last_price = None
        self.last_date = None
        self.buy_volume = 0
        self.close_price = [float(i) for i in self.config.get("Strategy", "ClosePrice").split(',')]

    # Process Market Data. Please use onOHLCFeed() in OHLC mode
    def onMarketDataUpdate(self, market, code, md):

        time_info = md.timestamp.split('_')
        if int(time_info[1]) not in (range(93000, 120000) + range(130000, 160000)):
            return

        # For open price
        if time_info[0] != self.last_date:
            self.last_date = time_info[0]

            if self.last_price:
                self.close_price.pop(0)
                self.close_price.append(self.last_price)

        mean_average = talib.MA(numpy.array(self.close_price), self.move_average_day)[-1]
        standard_dev = talib.STDDEV(numpy.array(self.close_price))[-1]

        if md.lastPrice < 1:
            md.lastPrice *= 100
        if md.lastPrice + self.factor * standard_dev < mean_average:
            volume = int(self.total_capital / 10 / md.lastPrice)
            if self.current_capital > self.total_capital / 10:
                order = cashAlgoAPI.Order(md.timestamp, 'SEHK', code, str(self.cnt), md.askPrice1, volume,
                                          "open", 1, "insert", "market_order", "today")

                self.mgr.insertOrder(order)
                self.cnt += 1
                self.buy_volume += volume
                self.current_capital -= volume * md.askPrice1
                print "Buy: %s %s" % (volume, self.total_capital)

        if int(10 * md.lastPrice) >= int(mean_average * 10) and self.buy_volume:
            order = cashAlgoAPI.Order(md.timestamp, 'SEHK', code, str(self.cnt), md.bidPrice1, self.buy_volume,
                                      "open", 2, "insert", "market_order", "today")

            self.mgr.insertOrder(order)
            self.cnt += 1
            self.current_capital += self.buy_volume * md.bidPrice1
            self.total_capital = self.current_capital
            print "Sell: %s %s" % (self.buy_volume, self.total_capital)
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
        pass
        # print "Trade feed: %s price: %s, timestamp: %s volume: %s" % (tf.buySell, tf.price, tf.timestamp, tf.volume)

    # Process Position
    def onPortfolioFeed(self, portfolioFeed):
        pass

    # Process PnL
    def onPnlperffeed(self, pf):
        # print "dailyPnL: %s" % pf.dailyPnL
        pass

