import yfinance as yf
import pandas as pd

sp500_url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
table = pd.read_html(sp500_url)
sp500_df = table[0]
tickers = sp500_df["Symbol"].tolist()

tickers = [ticker.replace('.', '-') for ticker in tickers]
data = yf.download(tickers, period="1y", interval="1d", group_by='ticker')

data.to_csv("sp500_stock_data.csv")
print("CSV file saved as sp500_stock_data.csv")
