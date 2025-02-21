import yfinance as yf

# Define stock symbols
stocks = ["AAPL", "MSFT"]

# Fetch data for the last year
data = yf.download(stocks, period="1y", interval="1d")

# Save to CSV
data.to_csv("apple_microsoft_full_stock_data.csv")

print("CSV file saved as apple_microsoft_full_stock_data.csv")
