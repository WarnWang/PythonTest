import cashAlgoAPI
import CardsLib
import CardsILib
import talib
import numpy


class Strategy:
    # varible:
    # self.mgr: order manager
    # self.config: configuration reader from parameter panel

    # Initialize Strategy
    def init(self):
        self.cnt = 0

        # Read Parameters
        self.low = {}
        self.high = {}
        self.open = {}
        self.close = {}
        self.pos = {}
        self.bettingSize = {}
        self.perBetAmt = float(self.config.get("Strategy", "perBetAmt"))
        for i in range(1, 10):
            if self.config.has_option("MarketData", "ProductCode_%d" % i):
                self.low[str(self.config.get("MarketData", "ProductCode_%d" % i))] = []
                self.high[str(self.config.get("MarketData", "ProductCode_%d" % i))] = []
                self.open[str(self.config.get("MarketData", "ProductCode_%d" % i))] = []
                self.close[str(self.config.get("MarketData", "ProductCode_%d" % i))] = []
                self.bettingSize[str(self.config.get("MarketData", "ProductCode_%d" % i))] = []
                self.pos[str(self.config.get("MarketData", "ProductCode_%d" % i))] = 0
        self.forceClose = False
        # Process Market Data. Please use onOHLCFeed() in OHLC mode

        help(CardsILib)
        help(CardsLib)
        help(cashAlgoAPI)

    def onMarketDataUpdate(self, market, code, md):
        return

    # Used in OHLC mode.
    def onOHLCFeed(self, of):
        if of.timestamp[9:15] <= "093000" or of.timestamp[9:15] >= "155000":
            return
        if "120000" <= of.timestamp[9:15] <= "130000":
            return
        if of.timestamp[0:8] == "20150331":
            self.forceClose = True
        self.open[of.productCode].append(of.open)
        self.high[of.productCode].append(of.high)
        self.low[of.productCode].append(of.low)
        self.close[of.productCode].append(of.close)

        if len(self.open[of.productCode]) > 10:
            self.open[of.productCode].pop(0)
            self.high[of.productCode].pop(0)
            self.low[of.productCode].pop(0)
            self.close[of.productCode].pop(0)
        open = numpy.array(self.open[of.productCode], dtype=float)
        high = numpy.array(self.high[of.productCode], dtype=float)
        low = numpy.array(self.low[of.productCode], dtype=float)
        close = numpy.array(self.close[of.productCode], dtype=float)

        val = talib.CDLENGULFING(open, high, low, close)
        signal = val[-1]
        if signal < 0 and self.pos[of.productCode] == 0 and not self.forceClose:
            self.bettingSize[of.productCode] = self.perBetAmt / of.close
            order = cashAlgoAPI.Order(of.timestamp, "SEHK", of.productCode, str(self.cnt), of.close,
                                      self.bettingSize[of.productCode], "open", 1, "insert", "market_order", "today")
            print "Place an BUY order at %s %s" % (of.timestamp, of.productCode)
            self.pos[of.productCode] = 1

            self.mgr.insertOrder(order)
            self.cnt += 1
        if (signal > 0 or self.forceClose) and self.pos[of.productCode] > 0:
            order = cashAlgoAPI.Order(of.timestamp, "SEHK", of.productCode, str(self.cnt), of.close,
                                      self.bettingSize[of.productCode], "open", 2, "insert", "market_order", "today")
            print "Place an SELL order at %s %s" % (of.timestamp, of.productCode)
            self.pos[of.productCode] = 0
            self.mgr.insertOrder(order)
            self.cnt += 1
        return

    # Process Order
    def onOrderFeed(self, of):
        return

    # Process Trade
    def onTradeFeed(self, tf):
        return

    # Process Position
    def onPortfolioFeed(self, portfolioFeed):
        return

    # Process PnL
    def onPnlperffeed(self, pf):
        return
