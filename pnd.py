import pandas as pd

df = pd.read_csv("full_stock_data.csv")

print(df.head())
print(df.columns)

#see if there's correlation between cloing from like a few days ago and today