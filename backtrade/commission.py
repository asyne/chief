from backtrader.commissions import CommInfoBase


class BinaryCommission(CommInfoBase):
    params = (
        (profitability=0.8)
    )

    def _getcommission(self, size, price, pseudoexec):
        import pdb; pdb.set_trace()
        return 0
