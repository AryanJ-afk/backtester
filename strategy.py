from event import SignalEvent

class MomentumStrategy:
    def __init__(self, events, data, symbol, lookback=90):
        self.events, self.data, self.symbol = events, data, symbol
        self.lookback = lookback
        self.invested = False

    def calculate_signals(self):
        closes = [b[1]["close"] for b in self.data.latest_bars]
        if len(closes) < self.lookback + 1:
            return
        dt = self.data.get_latest_datetime()
        if closes[-1] > closes[-self.lookback] and not self.invested:
            self.events.put(SignalEvent(self.symbol, dt, "LONG")); self.invested = True
        elif closes[-1] < closes[-self.lookback] and self.invested:
            self.events.put(SignalEvent(self.symbol, dt, "EXIT")); self.invested = False


class MovingAverageStrategy:
    def __init__(self, events, data, symbol, short=20, long=50):
        self.events = events
        self.data = data          # DataHandler
        self.symbol = symbol
        self.short = short
        self.long = long
        self.invested = False

    def calculate_signals(self):
        closes = [bar[1]["close"] for bar in self.data.latest_bars]
        if len(closes) < self.long:
            return                 # not enough history yet

        short_ma = sum(closes[-self.short:]) / self.short
        long_ma = sum(closes[-self.long:]) / self.long
        dt = self.data.get_latest_datetime()

        if short_ma > long_ma and not self.invested:
            self.events.put(SignalEvent(self.symbol, dt, "LONG"))
            self.invested = True
        elif short_ma < long_ma and self.invested:
            self.events.put(SignalEvent(self.symbol, dt, "EXIT"))
            self.invested = False