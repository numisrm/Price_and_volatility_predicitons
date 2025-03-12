import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

df_high = pd.read_csv('high_data.csv')
df_low = pd.read_csv('low_data.csv')

df_high['Date'] = pd.to_datetime(df_high['Date'])
df_low['Date'] = pd.to_datetime(df_low['Date'])

df = pd.merge(df_high, df_low, on='Date', suffixes=('_High', '_Low'))
df.set_index('Date', inplace=True)
tickers = [col.replace('_High', '') for col in df_high.columns if col != 'Date']

weekly_results = []

for week_start, group in df.resample('W'):
    if len(group) == 0:
        continue

    N = len(group)
    week_vol = {"Week": week_start}
    
    for ticker in tickers:
        high_col = f"{ticker}_High"
        low_col = f"{ticker}_Low"        
        log_ratio = np.log(group[high_col] / group[low_col])
        squared_log_ratio = log_ratio ** 2
        sigma = np.sqrt((1 / (4 * np.log(2) * N)) * squared_log_ratio.sum())
        week_vol[ticker] = sigma
    
    weekly_results.append(week_vol)

weekly_vol_df = pd.DataFrame(weekly_results)
weekly_vol_df.sort_values("Week", inplace=True)
print(weekly_vol_df)


weekly_vol_df['Week'] = pd.to_datetime(weekly_vol_df['Week'])

# Set the Week column as the index for plotting convenience
weekly_vol_df.set_index('Week', inplace=True)

# Plot settings
plt.figure(figsize=(12, 6))
for ticker in weekly_vol_df.columns:
    plt.plot(weekly_vol_df.index, weekly_vol_df[ticker], marker='o', label=ticker)

plt.title("Weekly Parkinson Volatility by Ticker")
plt.xlabel("Week")
plt.ylabel("Volatility")
plt.legend(title="Ticker")
plt.grid(True)
plt.tight_layout()
plt.show()
