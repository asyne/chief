import numpy as np

from .indicator import Indicator
from .order import Order


class Strategy:
    open = []
    high = []
    low = []
    close = []

    def buy(self, amount, duration):
        self.broker._place_order(
            abs(amount),
            duration,
            Order.Type.Buy
        )

    def sell(self, amount, duration):
        self.broker._place_order(
            abs(amount),
            duration,
            Order.Type.Sell
        )

    def _do_bootstrap(self, dates, open, high, low, close):
        # initialize with data
        self.dates = dates
        self.open = open
        self.high = high
        self.low = low
        self.close = close

        self.lookback = 0  # overall strategy lookback based on all indicators
        self.indicators = []  # store indicators to auto-update their values for each timeframe

        for attr in self.__dict__.values():
            if isinstance(attr, Indicator):
                self.indicators.append(attr)

                # update minumum lookback
                if attr.lookback > self.lookback:
                    self.lookback = attr.lookback

        return self

    def _update_datas(self, *datas):
        self.open, self.high, self.low, self.close = datas

    def _pre_next(self):
        for indicator in self.indicators:
            indicator(self.close)
