import pandas as pd

df = pd.read_csv("full_stock_data.csv")

print(df.head())
print(df.columns)

#see if there's correlation between cloing from like a few days ago and today

# Extract column names (tickers) from the first row
tickers = df.iloc[0, 1:].values  # Skip the first column (Date)

# Remove first two rows (ticker row and empty row) and reset index
df = df[2:].reset_index(drop=True)

# Rename columns: first column as "Date" and others as tickers
df.columns = ["Date"] + list(tickers)

close_data = df.iloc[:, :11]

close_data.to_csv("close_data.csv", index=False)

# Display first few rows
print(close_data.head())
