import pandas as pd
import numpy as np
from arch import arch_model
import matplotlib.pyplot as plt

df = pd.read_csv("close_data.csv", parse_dates=['Date'])
df.set_index('Date', inplace=True)

returns = np.log(df / df.shift(1)).dropna()

stock = 'AAPL'
stock_returns = returns[stock]

window = 10
forecasted_vol = []

for i in range(window, len(stock_returns)):
    train = stock_returns[i-window:i]
    model = arch_model(train, vol='GARCH', p=1, q=1)
    res = model.fit(disp="off")
    forecast = res.forecast(horizon=1)
    vol = np.sqrt(forecast.variance.values[-1, 0])
    forecasted_vol.append(vol)

forecasted_vol = pd.Series(forecasted_vol, index=stock_returns.index[window:])

realized_vol = stock_returns.rolling(window).std()
realized_vol = realized_vol[window:]

# Plotting both
plt.figure(figsize=(12,6))
plt.plot(forecasted_vol, label="GARCH Forecasted Volatility")
plt.plot(realized_vol, label="Realized Volatility (10-day rolling)", linestyle='--')
plt.title(f"{stock} - Forecasted vs Realized Volatility")
plt.xlabel("Date")
plt.ylabel("Volatility (std dev)")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
