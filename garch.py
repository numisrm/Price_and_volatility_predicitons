import pandas as pd
import numpy as np
from arch import arch_model
from itertools import product
import matplotlib.pyplot as plt
import sys
import os
import warnings


warnings.filterwarnings("ignore")
sys.stderr = open(os.devnull, 'w')


df = pd.read_csv("average_close_sp500.csv", parse_dates=['Date'])
df.set_index('Date', inplace=True)

returns = np.log(df / df.shift(1)).dropna()
avg_returns = returns['Average Close']

p_values = [1, 2]
q_values = [1, 2]
mean_values = ['Constant', 'AR', 'Zero']

results_list = []
best_aic = np.inf
best_params = None

for p, q, mean_type in product(p_values, q_values, mean_values):
    try:
        model = arch_model(avg_returns, p=p, q=q, mean=mean_type, vol='GARCH', dist='normal', rescale=False)
        res = model.fit(disp='off')
        aic = res.aic

        results_list.append({
            'p': p,
            'q': q,
            'mean': mean_type,
            'AIC': aic
        })

        if aic < best_aic:
            best_aic = aic
            best_params = {'p': p, 'q': q, 'mean': mean_type, 'AIC': aic}

    except Exception:
        results_list.append({
            'p': p,
            'q': q,
            'mean': mean_type,
            'AIC': np.nan
        })

results_df = pd.DataFrame(results_list)
print("AIC for all models tested:")
print(results_df)

if best_params is not None:
    print("\nBest parameters for Average Close:", best_params)
    
    window = 10
    forecasted_vol = []

    for i in range(window, len(avg_returns)):
        train = avg_returns[i - window:i]
        model = arch_model(train, p=best_params['p'], q=best_params['q'],
                           mean=best_params['mean'], vol='GARCH', dist='normal')
        res = model.fit(disp='off')
        forecast = res.forecast(horizon=1)
        vol_forecast = np.sqrt(forecast.variance.values[-1, 0])
        forecasted_vol.append(vol_forecast)
    
    forecasted_vol = pd.Series(forecasted_vol, index=avg_returns.index[window:])
    realized_vol = avg_returns.rolling(window).std()[window:]

    plt.figure(figsize=(12, 6))
    plt.plot(forecasted_vol, label="GARCH Forecasted Volatility")
    plt.plot(realized_vol, label="Realized Volatility (10-day rolling)", linestyle='--')
    plt.title("S&P 500 Average Close - Forecasted vs Realized Volatility")
    plt.xlabel("Date")
    plt.ylabel("Volatility (Std Dev of Log Returns)")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

else:
    print("No valid GARCH model found.")
