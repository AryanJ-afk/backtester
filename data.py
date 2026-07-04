import pandas as pd
from event import MarketEvent


class DataHandler:
    def __init__(self, events, csv_path, symbol):
        self.events = events          # the shared event queue
        self.symbol = symbol
        self.data = pd.read_csv(csv_path, index_col=0, parse_dates=True)
        self.data = self.data.sort_index()
        self._stream = self.data.iterrows()   # generator over rows
        self.latest_bars = []                 # bars revealed so far
        self.continue_backtest = True

    def update_bars(self):
        """Push the next bar onto latest_bars and fire a MarketEvent."""
        try:
            timestamp, row = next(self._stream)
        except StopIteration:
            self.continue_backtest = False
            return
        self.latest_bars.append((timestamp, row))
        self.events.put(MarketEvent())

    def get_latest_close(self):
        """Most recent close price — strategy/portfolio query this."""
        return self.latest_bars[-1][1]["close"]

    def get_latest_datetime(self):
        return self.latest_bars[-1][0]