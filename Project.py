import yfinance as yf

stocks = ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA", "NVDA", "META", "BRK-B", "V", "JNJ"]

data = yf.download(stocks, period="1y", interval="1d")

data.to_csv("apple_microsoft_full_stock_data.csv")

print("CSV file saved as apple_microsoft_full_stock_data.csv")
