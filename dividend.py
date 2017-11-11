import pandas as pd
import numpy as np
import quandl
import datetime
quandl.ApiConfig.api_key = 'xRMzJd1KP8azFCp-y-jH'

def get_historical(ticker, interval = ["2000-06-28", "2017-05-25"]):
    return quandl.get(ticker, start_date = interval[0], end_date = interval[1])

#collect 
def normalize_dividends(history):
    history = history.copy()
    history['Adj. Dividend'] = 0 
    current_split = 1.0
    for index in reversed(history.index):
        if history['Split Ratio'][index] != 1.0:
            current_split *= history['Split Ratio'][index]
            history.loc[index, 'Adj. Dividend'] = history['Ex-Dividend'][index] / current_split
            
        else:
            history.loc[index, 'Adj. Dividend'] = history['Ex-Dividend'][index] / current_split    
        
    return history
        

#find the dividend policy in a given year
def dividend_policy(history, year):
    temp_history = set_index_by(history);
    dividend_list = [i for i in temp_history.loc[year, 'Ex-Dividend'] if i != 0]
    if len(dividend_list) == 4:
        return 'Quarterly'
    else:
        return False
        #raise 
      

def set_index_by(history):
    history['year'] = pd.DatetimeIndex(df.index).year
    history['month'] = pd.DatetimeIndex(df.index).month
    #history['date'] = pd.DatetimeIndex(df.index).date
    
    return df.set_index(['year', 'month'])


df = get_historical('WIKI/AAPL')
df1 = normalize_dividends(df)
print(dividend_policy(df, [2015]))

