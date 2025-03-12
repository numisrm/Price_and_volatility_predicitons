import pandas as pd

df = pd.read_csv('full_stock_data.csv', header=[0, 1, 2])

dates = df.iloc[:, 0]

df_high = pd.DataFrame()
df_low = pd.DataFrame()

df_high['Date'] = dates
df_low['Date'] = dates

high_cols = df.columns.get_level_values(0) == 'High'
low_cols = df.columns.get_level_values(0) == 'Low'

for col in df.columns[high_cols]:
    ticker = col[1] 
    new_col_name = f"{ticker}_High"
    df_high[new_col_name] = df[col]

for col in df.columns[low_cols]:
    ticker = col[1]
    new_col_name = f"{ticker}_Low"
    df_low[new_col_name] = df[col]

df_high.to_csv('high_data.csv', index=False)
df_low.to_csv('low_data.csv', index=False)
