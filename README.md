# Event-Driven Backtester

A minimal event-driven backtesting engine in Python. Simulates trading strategies on historical stock data using a market/signal/order/fill event queue, which prevents look-ahead bias by construction.

## Features

- Event-driven architecture (components communicate only via events)
- Realistic execution with slippage and commission
- Equity-based position sizing (95% of capital per trade)
- Performance metrics: Sharpe ratio, max drawdown, total return, vs. buy-and-hold benchmark

## Strategies

- **Moving Average Crossover** — long when short MA crosses above long MA, exit on cross back
- **Momentum** — long when price exceeds its value N days ago, exit otherwise

## Structure

```
backtester/
├── event.py        # Event types: Market, Signal, Order, Fill
├── data.py         # DataHandler: feeds bars one at a time
├── strategy.py     # Strategies: consume market data, emit signals
├── portfolio.py    # Portfolio: signals to orders, tracks positions/cash/PnL
├── execution.py    # ExecutionHandler: orders to fills (slippage + costs)
├── metrics.py      # Performance metrics
└── engine.py       # Event loop
```

## Setup

```bash
pip install pandas numpy yfinance
```

Download data:

```python
import yfinance as yf
df = yf.download("AAPL", start="2015-01-01", end="2024-01-01")
df.columns = df.columns.get_level_values(0).str.lower()
df.to_csv("data.csv")
```

## Run

```bash
python engine.py
```

Prints metrics for each strategy against a buy-and-hold benchmark.