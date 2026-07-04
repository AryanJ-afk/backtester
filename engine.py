import queue
from data import DataHandler
from strategy import MovingAverageStrategy, RSIStrategy, MomentumStrategy, BollingerStrategy
from portfolio import Portfolio
from execution import ExecutionHandler
from metrics import compute_metrics, buy_hold_return


def run(csv_path, symbol, strategy_class):
    events = queue.Queue()
    data = DataHandler(events, csv_path, symbol)
    strategy = strategy_class(events, data, symbol)
    portfolio = Portfolio(events, data, symbol)
    execution = ExecutionHandler(events, data, symbol)

    while data.continue_backtest:
        data.update_bars()
        while True:
            try:
                event = events.get(False)
            except queue.Empty:
                break
            if event.type == "MARKET":
                strategy.calculate_signals()
                portfolio.update_equity()
            elif event.type == "SIGNAL":
                portfolio.update_signal(event)
            elif event.type == "ORDER":
                execution.execute_order(event)
            elif event.type == "FILL":
                portfolio.update_fill(event)

    m = compute_metrics(portfolio.equity_curve)
    m["buy_hold"] = buy_hold_return(portfolio.equity_curve, data)
    return m


if __name__ == "__main__":
    for s in [MovingAverageStrategy, MomentumStrategy]:
        print(s.__name__, run("data.csv", "AAPL", s))