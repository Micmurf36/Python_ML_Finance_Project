#This is the main script to update the database every five minutes. Place in alpine docker container then run in venv and set task to run every 5 minutes with cron. 


from alpha_vantage.timeseries import TimeSeries
import pandas as pd
from sqlalchemy import create_engine
from datetime import datetime, timedelta

# Your Alpha Vantage API Key and other details
api_key = ''
symbol = ''
interval = ''

# Database connection details
username = ''
password = ''
host = ''
port = ''
database = ''

# SQLAlchemy engine for MySQL
engine = create_engine(f'mysql+mysqlconnector://{username}:{password}@{host}:{port}/{database}')

# Make an API call for the most recent data
ts = TimeSeries(key=api_key, output_format='pandas')
data, meta_data = ts.get_intraday(symbol=symbol, interval=interval, outputsize='compact')

# Renaming the DataFrame columns to match the SQL table column names
data.reset_index(inplace=True)
data.columns = ['date', 'open', 'high', 'low', 'close', 'volume']

# Convert 'date' column to datetime format and then to string for SQL compatibility
data['date'] = pd.to_datetime(data['date']).dt.strftime('%Y-%m-%d %H:%M:%S')

# Get existing dates from the database
existing_dates_query = "SELECT date FROM eurusd_prices"
existing_dates = pd.read_sql(existing_dates_query, con=engine)
existing_dates_set = set(existing_dates['date'].astype(str))

# Filter out data that already exists
new_data = data[~data['date'].isin(existing_dates_set)]

# Insert new data into the database
if not new_data.empty:
    new_data.to_sql(name='eurusd_prices', con=engine, if_exists='append', index=False)

# Save the data to a CSV file (optional)
#data.to_csv('eurusd_complete_data.csv')

# Print the first few rows of the DataFrame
print(data.head())
