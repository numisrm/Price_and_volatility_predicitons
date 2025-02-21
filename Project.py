import yfinance as yf

ticker = "AAPL"
stock = yf.Ticker(ticker)

appl = yf.download("AAPL", start="2023-01-01", end="2023-06-30")

print(type(appl))
