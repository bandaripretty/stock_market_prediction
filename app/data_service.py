import pandas as pd
import psycopg2
from sklearn.linear_model import LinearRegression

# Function to fetch stock data
def fetch_stock_data(symbol, start_date=None, end_date=None):
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="stock_market",
            user="postgres",
            password="T!m3L1n3@Secure#2024",
            port="5433"
        )
        cur = conn.cursor()

        if start_date and end_date:
            cur.execute("""
                SELECT date, open, close, high, low, volume FROM PriceData
                WHERE stock_id = (SELECT stock_id FROM Stock WHERE symbol = %s)
                AND date BETWEEN %s AND %s
            """, (symbol, start_date, end_date))
        else:
            cur.execute("""
                SELECT date, open, close, high, low, volume FROM PriceData
                WHERE stock_id = (SELECT stock_id FROM Stock WHERE symbol = %s)
            """, (symbol,))

        data = cur.fetchall()
        conn.close()

        if not data:
            return None

        # Convert to dict
        stock_data = {
            'open': data[0][1],
            'close': data[0][2],
            'high': data[0][3],
            'low': data[0][4],
            'volume': data[0][5]
        }
        return stock_data

    except Exception as e:
        return {"error": str(e)}

# Function to predict stock prices using Linear Regression
def predict_stock_price(symbol):
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="stock_market",
            user="postgres",
            password="T!m3L1n3@Secure#2024",
            port="5433"
        )
        cur = conn.cursor()

        cur.execute("""
            SELECT date, close FROM PriceData
            WHERE stock_id = (SELECT stock_id FROM Stock WHERE symbol = %s)
            ORDER BY date
        """, (symbol,))
        data = cur.fetchall()
        conn.close()

        if not data:
            return None

        df = pd.DataFrame(data, columns=['date', 'close'])
        df['date'] = pd.to_datetime(df['date'])
        df['date_ordinal'] = df['date'].apply(lambda x: x.toordinal())

        # Create Linear Regression model
        X = df[['date_ordinal']]
        y = df['close']
        model = LinearRegression()
        model.fit(X, y)

        # Predict for the next 5 days
        future_dates = pd.date_range(start=df['date'].max(), periods=5).to_frame(index=False, name='date')
        future_dates['date_ordinal'] = future_dates['date'].apply(lambda x: x.toordinal())
        predicted_prices = model.predict(future_dates[['date_ordinal']])

        return {
            "predicted_dates": future_dates['date'].dt.strftime('%Y-%m-%d').tolist(),
            "predicted_prices": predicted_prices.tolist()
        }

    except Exception as e:
        return {"error": str(e)}
