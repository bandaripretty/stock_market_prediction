import matplotlib.pyplot as plt
import pandas as pd
from sqlalchemy import create_engine

# Connect to PostgreSQL
engine = create_engine('postgresql://postgres:1712@localhost/stock_data')

def create_line_graph(symbol):
    query = f"SELECT date, close FROM stock_prices WHERE symbol = '{symbol}' ORDER BY date"
    df = pd.read_sql(query, engine)

    # Plot line graph for closing prices
    plt.figure(figsize=(10, 5))
    plt.plot(df['date'], df['close'], label=f'{symbol} Closing Price', color='blue')
    plt.title(f'{symbol} Stock Closing Prices Over Time')
    plt.xlabel('Date')
    plt.ylabel('Closing Price (USD)')
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Save the graph as an image
    plt.savefig(f'static/{symbol}_closing_price.png')
    plt.close()

def create_pie_chart():
    query = "SELECT symbol, SUM(volume) AS total_volume FROM stock_prices GROUP BY symbol"
    df = pd.read_sql(query, engine)

    # Plot pie chart for total volumes
    plt.figure(figsize=(7, 7))
    plt.pie(df['total_volume'], labels=df['symbol'], autopct='%1.1f%%', startangle=140)
    plt.title('Stock Volume Distribution by Company')
    
    # Save the pie chart as an image
    plt.savefig('static/volume_distribution.png')
    plt.close()

# Example usage for multiple companies
symbols = ['AAPL', 'GOOG', 'MSFT', 'TSLA']
for symbol in symbols:
    create_line_graph(symbol)

create_pie_chart()