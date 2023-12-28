#use this script to check what you are getting. If looks good move to below script for moving historical to mysql
from alpha_vantage.timeseries import TimeSeries
import pandas as pd
from datetime import datetime, timedelta

api_key = ''
symbol = ''
interval = '5min'

# Make a single API call
ts = TimeSeries(key=api_key, output_format='pandas')
data, meta_data = ts.get_intraday(symbol=symbol, interval=interval, outputsize='full')

# Save the data to a CSV file
data.to_csv('eurusd_complete_data.csv')

# Print the first few rows of the DataFrame
print(data)
