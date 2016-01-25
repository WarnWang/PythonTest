# Import the core module
import cashAlgoAPI


# Declare and implement a class: Strategy
class Strategy:
    def __init__(self):
        self.cnt = 0
        self.last_date = None
        self.range = 0
        self.min = 0
        self.min_range = 0
        self.max_range = 0
        self.list = []
        self.position = 0
        self.target = 0
        self.open_price = 0

    # Initialize Strategy
    def init(self):
        self.min = self.config.get("Strategy", "min")
        self.min_range = float(self.config.get("Strategy", "minrange"))
        self.max_range = float(self.config.get("Strategy", "maxrange"))

    # Process Market Data.
    def onMarketDataUpdate(self, market, code, md):
        if int(md.timestamp[9:11]) not in range(9, 12) + range(13, 17):
            return

        if self.last_date != md.timestamp[0:8]:
            self.last_date = md.timestamp[0:8]
            self.list = []
            self.position = 0
            self.target = 0
            self.open_price = 0

        if 1 <= md.lastPrice < 999999:
            if len(self.list) >= self.min:
                self.list.pop(0)
            self.list.append(md.lastPrice)

            max_price = max(self.list)
            min_price = min(self.list)
            self.range = max_price - min_price

            if self.max_range >= self.range >= self.min_range and self.position == 0:
                if md.lastPrice >= max_price:
                    order = cashAlgoAPI.Order(md.timestamp, md.market, md.productCode, str(self.cnt), md.askPrice1, 1,
                                              "open", 1, "insert", "market_order", "today")
                    self.mgr.insertOrder(order)
                    self.cnt += 1
                    self.position = 1
                    self.target = self.range
                    self.open_price = md.askPrice1

                if md.lastPrice <= min_price:
                    order = cashAlgoAPI.Order(md.timestamp, md.market, md.productCode, str(self.cnt), md.bidPrice1, 1,
                                              "open", 2, "insert", "market_order", "today")
                    self.mgr.insertOrder(order)

                    self.cnt += 1
                    self.position = -1
                    self.target = self.range
                    self.open_price = md.bidPrice1

            elif self.position == 1 and (md.lastPrice >= (self.open_price + self.target) or
                                                 md.lastPrice <= min_price or md.timestamp[9:13] == "1614"):
                order = cashAlgoAPI.Order(md.timestamp, md.market, md.productCode, str(self.cnt), md.bidPrice1, 1,
                                          "open", 2, "insert", "market_order", "today")
                self.mgr.insertOrder(order)

                self.cnt += 1
                self.position -= 1

            elif self.position == -1 and (md.lastPrice <= (self.open_price - self.target) or
                                                  md.lastPrice >= max_price or md.timestamp[9:13] == "1614"):
                order = cashAlgoAPI.Order(md.timestamp, md.market, md.productCode, str(self.cnt), md.askPrice1, 1,
                                          "open", 1, "insert", "market_order", "today")
                self.mgr.insertOrder(order)
                self.cnt += 1
                self.position += 1

    # Used in OHLC mode.
    def onOHLCFeed(self, of):
        md = cashAlgoAPI.MarketData([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
        md.timestamp = of.timestamp
        md.market = of.market
        md.productCode = str(of.productCode)
        md.lastPrice = of.close
        md.askPrice1 = of.close
        md.bidPrice1 = of.close
        md.lastVolume = 1

        self.onMarketDataUpdate("", of.productCode, md)

    # Process Order
    def onOrderFeed(self, of):
        pass

    # Process Trade
    def onTradeFeed(self, tf):
        pass

    # Process Position
    def onPortfolioFeed(self, portfolioFeed):
        pass

    # Process PnL
    def onPnlperffeed(self, pf):
        pass
