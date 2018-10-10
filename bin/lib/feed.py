import pandas as pd

from .timeframe import TimeFrame


class DataFeed:

    def __init__(self, path, timeframe=TimeFrame.Minutes):
        df = pd.read_csv(path)

        self.dates = df['Date'].values
        self.open = df['Open'].values
        self.high = df['High'].values
        self.low = df['Low'].values
        self.close = df['Close'].values
