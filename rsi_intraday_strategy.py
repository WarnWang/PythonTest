#!/usr/bin/python
# -*- coding: utf-8 -*-

# File name: macd_strategy
# Author: warn
# Date: 25/12/2015 13:00

import cashAlgoAPI
import numpy
import talib


class Strategy:
    long_flag = False
    short_flag = False

    def __init__(self):
        self.close_data = []
        self.cnt = 0
        self.last_data = None
        self.data_number = None
        self.rsi_period = None
        self.hold_volume = 0
        self.total_capital = 0
        self.current_capital = 0

    def init(self):
        self.cnt = 0
        self.close_data = []
        self.hold_volume = 0
        self.data_number = int(self.config.get("Strategy", "MaxDataNumber"))
        self.rsi_period = int(self.config.get("Strategy", "RsiPeriod"))
        self.current_capital = self.total_capital = float(self.config.get("Risk", "InitialCapital"))

    def onMarketDataUpdate(self, market, code, md):

        # The following time is not allowed to trade. Only trade from 9:30 am to 12:00 am, and from 13:00 to 16:00
        time_info = md.timestamp.split('_')
        if not (int(time_info[1][:2]) in (range(10, 12) + range(13, 16)) or
                    (time_info[1][:2] == '09' and int(time_info[1][2:]) >= 3000) or
                        time_info[1][:4] == '1600'):
            return

        # Open price clear all the data
        if self.last_data != time_info[0]:
            self.last_data = time_info[0]
            self.close_data = []

        if len(self.close_data) >= self.data_number:
            self.close_data.pop(0)

        self.close_data.append(md.lastPrice)

        if len(self.close_data) >= self.rsi_period:
            rsi_result = talib.RSI(numpy.array(self.close_data), timeperiod=self.rsi_period)[-1]
            if rsi_result < 30 and not self.long_flag:
                self.long_flag = True
                self.short_flag = False
            elif self.long_flag and 70 > rsi_result >= 30:
                self.long_flag = False
                volume = self.total_capital / 10 / md.lastPrice
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

        if self.hold_volume and md.timestamp.split('_')[1][:4] == '1600':
            print "Close market at %s, and sell all the belongings" % md.timestamp
            self.short_security(md.timestamp, code, md.lastPrice)
            self.short_flag = False
            self.long_flag = False

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
        # print "feed price of %s is %s" % (of.productCode, of.close)
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
