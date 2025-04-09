import pandas as pd
import numpy as np
from arch import arch_model
from itertools import product
import matplotlib.pyplot as plt
import warnings
from arch.univariate.base import DataScaleWarning
warnings.simplefilter("ignore", DataScaleWarning)


df = pd.read_csv("close_data.csv", parse_dates=['Date'])
df.set_index('Date', inplace=True)

returns = np.log(df / df.shift(1)).dropna()

p_values = [1, 2]
q_values = [1, 2] 


results_list = []
best_params_dict = {}  
stock = 'AAPL'

stock_returns = returns[stock].dropna()
best_aic = np.inf
best_params = None

for p, q in product(p_values, q_values):
    try:
        model = arch_model(stock_returns, p=p, q=q, mean='Constant', vol='GARCH', dist='normal', rescale=False)
        res = model.fit(disp='off')
        aic = res.aic

        results_list.append({
            'Stock': stock,
            'p': p,
            'q': q,
            'AIC': aic
        })

        if aic < best_aic:
            best_aic = aic
            best_params = {'p': p, 'q': q, 'AIC': aic}

    except Exception as e:
        results_list.append({
            'Stock': stock,
            'p': p,
            'q': q,
            'AIC': np.nan
        })
best_params_dict[stock] = best_params

results_df = pd.DataFrame(results_list)
print("AIC for all models tested:")
print(results_df)

if stock in best_params_dict and best_params_dict[stock] is not None:
    params = best_params_dict[stock]
    print("\nBest parameters for", stock, ":", params)
    
    stock_returns = returns[stock].dropna()
    window = 10 
    forecasted_vol = []

    for i in range(window, len(stock_returns)):
        train = stock_returns[i - window:i]
        model = arch_model(train, p=params['p'], q=params['q'],
                           mean='Constant', vol='GARCH', dist='normal')
        res = model.fit(disp='off')
        forecast = res.forecast(horizon=1)
        vol_forecast = np.sqrt(forecast.variance.values[-1, 0])
        forecasted_vol.append(vol_forecast)
    
    forecasted_vol = pd.Series(forecasted_vol, index=stock_returns.index[window:])

    realized_vol = stock_returns.rolling(window).std()[window:]

    plt.figure(figsize=(12, 6))
    plt.plot(forecasted_vol, label="GARCH Forecasted Volatility")
    plt.plot(realized_vol, label="Realized Volatility (10-day rolling)", linestyle='--')
    plt.title(f"{stock} - Forecasted vs Realized Volatility (Optimized p and q)")
    plt.xlabel("Date")
    plt.ylabel("Volatility (Std Dev of Log Returns)")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

else:
    print(f"No valid best model found for {stock}.")