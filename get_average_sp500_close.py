import yfinance as yf
import pandas as pd

sp500_url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
table = pd.read_html(sp500_url)
sp500_df = table[0]
tickers = sp500_df["Symbol"].str.replace('.', '-', regex=False).tolist()

df = yf.download(tickers, period="1y", interval="1d", group_by='ticker', auto_adjust=True)
close_df = df.xs('Close', axis=1, level=1)

close_df['Average Close'] = close_df.mean(axis=1)
close_df[['Average Close']].to_csv("average_close_sp500.csv")

print(close_df[['Average Close']].head())
