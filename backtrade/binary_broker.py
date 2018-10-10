import backtrader as bt


class BinaryBroker(bt.brokers.BackBroker):
    def _try_exec_market(self, order, popen, phigh, plow):
        return super()._try_exec_market(order, popen, phigh, plow)

    def _try_exec_historical(self, order):
        return super()._try_exec_historical(order)

    def _try_exec_limit(self, order, popen, phigh, plow, plimit):
        return super()._try_exec_limit(order, popen, phigh, plow, plimit)

    def _try_exec_stop(self, order, popen, phigh, plow, pcreated, pclose):
        return super()._try_exec_stop(order, popen, phigh, plow, pcreated, pclose)

    def _try_exec_stoplimit(self, order,
                            popen, phigh, plow, pclose,
                            pcreated, plimit):
        return super()._try_exec_stoplimit(order,
                                popen, phigh, plow, pclose,
                                pcreated, plimit)

    def _try_exec_close(self, order, pclose):
        return super()._try_exec_close(order, order, pclose)
