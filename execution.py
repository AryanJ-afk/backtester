from event import FillEvent


class ExecutionHandler:
    def __init__(self, events, data, symbol, commission=1.0, slippage=0.001):
        self.events = events
        self.data = data
        self.symbol = symbol
        self.commission = commission
        self.slippage = slippage      # fraction of price

    def execute_order(self, event):
        price = self.data.get_latest_close()
        if event.direction == "BUY":
            fill_price = price * (1 + self.slippage)
        else:
            fill_price = price * (1 - self.slippage)

        self.events.put(FillEvent(
            self.symbol,
            self.data.get_latest_datetime(),
            event.quantity,
            event.direction,
            fill_price,
            self.commission,
        ))