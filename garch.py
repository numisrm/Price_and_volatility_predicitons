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
dist_values = ['normal', 't']
window_values = [7,14]

results_list = []
best_error = np.inf
best_params = None

for p, q, mean_type, dist_type, window in product(p_values, q_values, mean_values, dist_values, window_values):
    try:
        print(f"Testing GARCH({p},{q}) with mean={mean_type}, dist={dist_type}, window={window}")
        forecasted_vol_list = []
        for i in range(window, len(avg_returns)):
            train = avg_returns.iloc[i - window:i]
            model = arch_model(train, p=p, q=q, mean=mean_type, vol='GARCH', dist=dist_type, rescale=False)
            res = model.fit(disp='off')
            forecast = res.forecast(horizon=1)
            vol_forecast = np.sqrt(forecast.variance.values[-1, 0])
            forecasted_vol_list.append(vol_forecast)
        
        forecasted_vol_series = pd.Series(forecasted_vol_list, index=avg_returns.index[window:])
        realized_vol_series = avg_returns.rolling(window).std().iloc[window:]
        forecasted_vol_series = forecasted_vol_series.loc[realized_vol_series.index]
        mse = np.mean((forecasted_vol_series - realized_vol_series) ** 2)
        
        results_list.append({
            'p': p,
            'q': q,
            'mean': mean_type,
            'dist': dist_type,
            'window': window,
            'MSE': mse
        })
        
        if mse < best_error:
            best_error = mse
            best_params = {'p': p, 'q': q, 'mean': mean_type, 'dist': dist_type, 'window': window, 'MSE': mse}
    
    except Exception:
        results_list.append({
            'p': p,
            'q': q,
            'mean': mean_type,
            'dist': dist_type,
            'window': window,
            'MSE': np.nan
        })

results_df = pd.DataFrame(results_list)
print("Forecast MSE for all models tested:")
print(results_df)

if best_params is not None:
    print("\nBest parameters for Average Close according to forecasting error (MSE):", best_params)
    
    best_window = best_params['window']
    forecasted_vol_list = []
    
    for i in range(best_window, len(avg_returns)):
        train = avg_returns.iloc[i - best_window:i]
        model = arch_model(train, p=best_params['p'], q=best_params['q'],
                           mean=best_params['mean'], vol='GARCH', dist=best_params['dist'], rescale=False)
        res = model.fit(disp='off')
        forecast = res.forecast(horizon=1)
        vol_forecast = np.sqrt(forecast.variance.values[-1, 0])
        forecasted_vol_list.append(vol_forecast)
    
    forecasted_vol_series = pd.Series(forecasted_vol_list, index=avg_returns.index[best_window:])
    realized_vol_series = avg_returns.rolling(best_window).std().iloc[best_window:]
    
    plt.figure(figsize=(12, 6))
    plt.plot(forecasted_vol_series, label="GARCH Forecasted Volatility")
    plt.plot(realized_vol_series, label="Realized Volatility (Rolling)")
    plt.title("S&P 500 Average Close - Forecasted vs Realized Volatility\n(Optimized Hyperparameters)")
    plt.xlabel("Date")
    plt.ylabel("Volatility (Std Dev of Log Returns)")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()
else:
    print("No valid GARCH model found.")
