from event import OrderEvent


class Portfolio:
    def __init__(self, events, data, symbol, initial_capital=100000):
        self.events = events
        self.data = data
        self.symbol = symbol
        self.cash = initial_capital
        self.position = 0            # units held
        self.equity_curve = []

    def update_signal(self, event):
        if event.direction == "LONG":
            price = self.data.get_latest_close()
            qty = int(0.95 * self.cash / price)
            self.events.put(OrderEvent(self.symbol, "MKT", qty, "BUY"))
        elif event.direction == "EXIT":
            self.events.put(OrderEvent(self.symbol, "MKT", self.position, "SELL"))

    def update_fill(self, event):
        if event.direction == "BUY":
            self.position += event.quantity
            self.cash -= event.fill_price * event.quantity + event.commission
        else:
            self.position -= event.quantity
            self.cash += event.fill_price * event.quantity - event.commission

    def update_equity(self):
        price = self.data.get_latest_close()
        total = self.cash + self.position * price
        self.equity_curve.append((self.data.get_latest_datetime(), total))