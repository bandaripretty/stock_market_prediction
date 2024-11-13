import yfinance as yf
import pandas as pd
from sqlalchemy import create_engine

# Connect to PostgreSQL
engine = create_engine('postgresql://postgres:T%21m3L1n3%40Secure%232024@localhost/stock_data')

def fetch_stock_data(symbol):
    stock = yf.Ticker(symbol)
    hist = stock.history(period="1y")  # Fetch the last year's data
    
    # Prepare the data for insertion
    hist.reset_index(inplace=True)
    hist['symbol'] = symbol
    hist.rename(columns={'Date': 'date', 'Open': 'open', 'High': 'high', 
                         'Low': 'low', 'Close': 'close', 'Volume': 'volume'}, inplace=True)
    
    # Insert into the PostgreSQL database
    hist[['date', 'open', 'high', 'low', 'close', 'volume', 'symbol']].to_sql('stock_prices', engine, if_exists='append', index=False)

# Fetch data for multiple companies
symbols = ['AAPL', 'GOOG', 'MSFT', 'TSLA']  # Add more symbols as needed
for symbol in symbols:
    fetch_stock_data(symbol)