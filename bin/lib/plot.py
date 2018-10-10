import matplotlib

matplotlib.use('TkAgg')

from matplotlib import pyplot as plt, dates as pltdates, finance

class PlotMixin:
    """Broker mixin to support plots."""

    def plot(self):
        dates = list(
            map(pltdates.datestr2num, self.dates[:self.position + 1])
        )
        values = zip(
            dates,
            self.open[:self.position + 1],
            self.close[:self.position + 1],
            self.high[:self.position + 1],
            self.low[:self.position + 1]
        )

        fig, ax = plt.subplots()
        fig.subplots_adjust(bottom=0.2)
        finance.candlestick_ochl(ax, values, width=60/86400)

        plt.plot(self.buy_orders['x'], self.buy_orders['y'], 'g^')
        plt.plot(self.sell_orders['x'], self.sell_orders['y'], 'rv')


        self._plot_indicators(dates)

        ax.xaxis_date()
        plt.setp(plt.gca().get_xticklabels(), rotation=45, horizontalalignment='right')

        plt.show()

    def _plot_indicators(self, dates):
        for strat in self.runstrats:
            for ind in strat.indicators:
                for ln in ind.get_lines():
                    plt.plot(dates, ln)


    def _add_buy_marker(self, position, value):
        self.buy_orders['x'].append(pltdates.datestr2num(self.dates[position]))
        self.buy_orders['y'].append(value)

    def _add_sell_marker(self, position, value):
        self.sell_orders['x'].append(pltdates.datestr2num(self.dates[position]))
        self.sell_orders['y'].append(value)
