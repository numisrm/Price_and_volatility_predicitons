import pandas as pd
import numpy as np

# Read close data
close = pd.read_csv("close_data.csv")

# Check which columns have non-numeric values
non_numeric = close.applymap(lambda x: not isinstance(x, (int, float))).any()
# print("Columns with non-numeric values:")
# print(non_numeric)
# All the data is numeric

def get_yearly_vol(column_name):
    
    data = close[column_name]

    daily_returns = np.array([])

    for i in range(len(data)-1):
        daily_returns = np.append(daily_returns, data[i+1] / data [i] - 1) 
    
    daily_vol = daily_returns.std()

    yearly_vol = daily_vol * np.sqrt(252)

    return yearly_vol

stocks = close.columns[1:]

yearly_volatilites = {x: float(get_yearly_vol(x)) for x in stocks}

print(yearly_volatilites)
