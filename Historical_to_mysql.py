#intial full request for historical data and move to mysql database  
from alpha_vantage.timeseries import TimeSeries
import pandas as pd
from sqlalchemy import create_engine

# Your Alpha Vantage API Key and other details
api_key = 'FFN37XQGG63KV2ZV'
symbol = 'EURUSD'
interval = '5min'

# Database connection details
username = 'root'  # replace with your MySQL username
password = 'Dinkingem187'  # replace with your MySQL password
host = '192.168.1.15'       # replace with your MySQL host IP
port = '3307'               # replace with your MySQL port
database = 'eurusd_data'    # your database name

# SQLAlchemy engine for MySQL
engine = create_engine(f'mysql+mysqlconnector://{username}:{password}@{host}:{port}/{database}')

# Make a single API call
ts = TimeSeries(key=api_key, output_format='pandas')
data, meta_data = ts.get_intraday(symbol=symbol, interval=interval, outputsize='full')

# Renaming the DataFrame columns to match the SQL table column names
data.columns = ['open', 'high', 'low', 'close', 'volume']

# Insert data into the database
data.to_sql(name='eurusd_prices', con=engine, if_exists='append', index=True, index_label='date')

# Save the data to a CSV file (optional, if you still want to save it as a CSV)
data.to_csv('eurusd_complete_data.csv')

# Print the first few rows of the DataFrame
print(data)
