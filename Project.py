import yfinance as yf

ticker = "AAPL"
stock = yf.Ticker(ticker)

hist = stock.history(period="5d")

print(hist)
