import yfinance as yf

df = yf.download("AAPL", start="2015-01-01", end="2024-01-01")
df.columns = df.columns.get_level_values(0).str.lower()      # DataHandler expects lowercase "close"
df.to_csv("data.csv")