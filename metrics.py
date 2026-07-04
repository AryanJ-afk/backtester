import numpy as np


def compute_metrics(equity_curve):
    values = [v for _, v in equity_curve]
    returns = np.diff(values) / values[:-1]

    total_return = (values[-1] - values[0]) / values[0]
    sharpe = np.sqrt(252) * returns.mean() / returns.std() if returns.std() > 0 else 0

    peak = np.maximum.accumulate(values)
    max_dd = ((values - peak) / peak).min()

    return {
        "total_return": total_return,
        "sharpe": sharpe,
        "max_drawdown": max_dd,
    }
    
def buy_hold_return(equity_curve, data):
    first = data.data["close"].iloc[0]
    last = data.data["close"].iloc[-1]
    return (last - first) / first