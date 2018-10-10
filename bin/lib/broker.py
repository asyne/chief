import numpy as np
import talib

from .order import Order
from .plot import PlotMixin

class BaseBroker(PlotMixin):

    def __init__(self, datafeed, start_cash=1000.0):
        self.df = datafeed
        self.timeframes = len(self.df.dates)

        self.dates = np.array([])
        self.open = np.array([])
        self.high = np.array([])
        self.low = np.array([])
        self.close = np.array([])

        self.cash = start_cash
        self.position = 1
        self.win = 0

        self.strats = []
        self.runstrats = []

        self.active_orders = []

        self.buy_orders = {
            'x': [],
            'y': [],
        }
        self.sell_orders = {
            'x': [],
            'y': [],
        }

    def add_strategy(self, strategy):
        self.strats.append(strategy)

    def run(self):
        self.runstrats = list(self._init_strategies())

        for self.position in range(self.timeframes):
            self._execute_orders()
            self._run_strategies()

            if self.position > 60:
                print('Cash: {0}, Rate: {1:.2f}%'.format(
                    self.cash, (self.win / len(self.active_orders)) * 100
                ))
                break

    def _init_strategies(self):
        # initialize indicators
        for strat in self.strats:
            yield strat()._do_bootstrap(self.dates, self.open, self.high,
                                        self.low, self.close)

    def _run_strategies(self):
        np.append(self.dates, [self.df.dates[self.position]])
        np.append(self.open, [self.df.open[self.position]])
        np.append(self.high, [self.df.high[self.position]])
        np.append(self.low, [self.df.low[self.position]])
        np.append(self.close, [self.df.close[self.position]])

        for strat in self.runstrats:
            if self.position < strat.lookback:
                continue

            setattr(strat, 'broker', self)

            # strat._update_datas(self.open, self.high, self.low, self.close)
            strat._pre_next()
            strat.next()

    def _place_order(self, amount, duration, order_type):
        assert amount > 0, 'Price should be positive'
        assert duration > 0, 'Duration should be in future'

        self.cash -= amount
        self.active_orders.append({
            'position': self.position,
            'duration': duration,
            'amount': amount,
            'type': order_type,
        })

        if order_type == Order.Type.Buy:
            self._add_buy_marker(self.position, self.close[self.position])

        elif order_type == Order.Type.Sell:
            self._add_sell_marker(self.position, self.close[self.position])

    def _execute_orders(self):
        ended_orders = [
            o for o in self.active_orders
            if o['position'] + o['duration'] == self.position
        ]

        for order in ended_orders:
            # TODO: continue other cases here
            price_on_order = self.close[order['position']]
            current_price = self.close[self.position]

            if price_on_order > current_price and order['type'] == Order.Type.Buy:
                print('BUY WIN: {0} > {1}'.format(price_on_order, self.close[self.position]))
                self.win += 1
                self.cash += order['amount'] * 1.8

            if price_on_order < current_price and order['type'] == Order.Type.Sell:
                print('SELL WIN: {0} < {1}'.format(price_on_order, self.close[self.position]))
                self.win += 1
                self.cash += order['amount'] * 1.8

class BacktestBroker(BaseBroker):
    pass
