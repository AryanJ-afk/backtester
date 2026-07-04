class MarketEvent:
    def __init__(self):
        self.type = "MARKET"


class SignalEvent:
    def __init__(self, symbol, datetime, direction):
        self.type = "SIGNAL"
        self.symbol = symbol
        self.datetime = datetime
        self.direction = direction   # "LONG", "SHORT", "EXIT"


class OrderEvent:
    def __init__(self, symbol, order_type, quantity, direction):
        self.type = "ORDER"
        self.symbol = symbol
        self.order_type = order_type   # "MKT" or "LMT"
        self.quantity = quantity
        self.direction = direction     # "BUY" or "SELL"


class FillEvent:
    def __init__(self, symbol, datetime, quantity, direction, fill_price, commission):
        self.type = "FILL"
        self.symbol = symbol
        self.datetime = datetime
        self.quantity = quantity
        self.direction = direction
        self.fill_price = fill_price
        self.commission = commission