import psycopg2
import yfinance as yf
from datetime import datetime, timedelta
import random

# Connect to PostgreSQL
conn = psycopg2.connect(
    host="localhost",
    database="stock_market",
    user="postgres",
    password="Nikhil@41",  # Use your actual password
    port="5433"
)
cur = conn.cursor()

# Step 1: Insert data into the Stock table
stock_symbols = [
    ('AAPL', 'Apple Inc.'),
    ('MSFT', 'Microsoft Corporation'),
    ('TSLA', 'Tesla, Inc.')
]

for symbol, name in stock_symbols:
    cur.execute("""
        INSERT INTO Stock (symbol, name)
        VALUES (%s, %s)
        ON CONFLICT (symbol) DO NOTHING;  -- Prevent duplicates
    """, (symbol, name))

# Commit the Stock insertion
conn.commit()

# Step 2: Insert data into the PriceData table for each stock
for symbol, name in stock_symbols:
    # Get stock_id for the current stock
    cur.execute("SELECT stock_id FROM Stock WHERE symbol = %s;", (symbol,))
    stock_id = cur.fetchone()[0]

    # Fetch stock data for the past year from Yahoo Finance
    data = yf.download(symbol, period="1y")

    for date, row in data.iterrows():
        # Convert each value to native Python types
        open_price = float(row['Open']) if row['Open'] is not None else None
        close_price = float(row['Close']) if row['Close'] is not None else None
        high_price = float(row['High']) if row['High'] is not None else None
        low_price = float(row['Low']) if row['Low'] is not None else None
        volume = int(row['Volume']) if row['Volume'] is not None else None
        adjusted_close = float(row['Adj Close']) if row['Adj Close'] is not None else None

        # Debugging: Check the types of the values being inserted
        print(f"Date: {date.date()}, Open: {open_price} ({type(open_price)}), "
              f"Close: {close_price} ({type(close_price)}), "
              f"High: {high_price} ({type(high_price)}), "
              f"Low: {low_price} ({type(low_price)}), "
              f"Volume: {volume} ({type(volume)}), "
              f"Adjusted Close: {adjusted_close} ({type(adjusted_close)})")

        # Insert into PriceData table
        cur.execute("""
            INSERT INTO PriceData (stock_id, date, open, close, high, low, volume, adjusted_close)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (stock_id, date.date(), open_price, close_price, high_price, low_price, volume, adjusted_close))

# Commit the PriceData insertion
conn.commit()

# Step 3: Simulate inserting data into the Prediction table (you can replace this with your actual prediction logic)
for symbol, name in stock_symbols:
    # Get stock_id for the current stock
    cur.execute("SELECT stock_id FROM Stock WHERE symbol = %s;", (symbol,))
    stock_id = cur.fetchone()[0]

    # Simulate 5 days of predictions
    for i in range(5):
        predicted_date = datetime.now().date() + timedelta(days=i + 1)
        predicted_price = random.uniform(150.0, 250.0)  # Simulate a random price prediction

        # Insert into Prediction table
        cur.execute("""
            INSERT INTO Prediction (stock_id, predicted_date, predicted_price)
            VALUES (%s, %s, %s)
        """, (stock_id, predicted_date, predicted_price))

# Commit the Prediction insertion
conn.commit()

# Close the cursor and connection
cur.close()
conn.close()

print("Data inserted successfully into Stock, PriceData, and Prediction tables.")
