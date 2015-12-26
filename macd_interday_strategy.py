#!/usr/bin/python
# -*- coding: utf-8 -*-

# File name: macd_strategy
# Author: warn
# Date: 25/12/2015 13:00

import cashAlgoAPI
import numpy
import talib


class Strategy:
    def __init__(self):
        self.close_data = []
        self.current_holding = False
        self.cnt = 0
        self.last_data = None
        self.last_price = None

    def init(self):
        self.cnt = 0
        self.current_holding = False
        close_data = self.config.get("Strategy", "close_data").split(',')
        self.close_data = [float(i) for i in close_data]

    def onMarketDataUpdate(self, market, code, md):
        time_info = md.timestamp.split('_')
        if self.last_data != time_info[0]:
            self.last_data = time_info[0]
            if self.last_price:
                self.close_data.pop(0)
                self.close_data.append(self.last_price)

            macd, macdsignal, mcadhist = talib.MACD(numpy.array(self.close_data), fastperiod=12, slowperiod=26,
                                                    signalperiod=9)
            if self.current_holding and macd[-1] < macdsignal[-1] < 0:
                order = cashAlgoAPI.Order(md.timestamp, 'SEHK', code, str(self.cnt),
                                          md.bidPrice1, 100, "open", 2, "insert",
                                          "market_order", "today")
                self.mgr.insertOrder(order)
                self.cnt += 1
                self.current_holding = False

            if not self.current_holding and macd[-1] > macdsignal[-1] > 0:
                order = cashAlgoAPI.Order(md.timestamp, 'SEHK', code, str(self.cnt),
                                          md.askPrice1, 100, "open", 1, "insert",
                                          "market_order", "today")
                self.mgr.insertOrder(order)
                self.cnt += 1
                self.current_holding = True

        self.last_price = float(md.lastPrice)

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
        # print "Trade feed: %s price: %s, timestamp: %s volume: %s" % (tf.buySell, tf.price, tf.timestamp, tf.volume)
        pass

    # Process Position
    def onPortfolioFeed(self, portfolioFeed):
        pass

    # Process PnL
    def onPnlperffeed(self, pf):
        # print "dailyPnL: %s" % pf.dailyPnL
        pass
