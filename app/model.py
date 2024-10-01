import pandas as pd
import psycopg2
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

# Fetch stock data from the database
def fetch_data(symbol):
    conn = psycopg2.connect(
        host="localhost",
        database="stock_market",
        user="postgres",
        password="T!m3L1n3@Secure#2024",
        port="5433"
    )
    cur = conn.cursor()
    cur.execute("SELECT date, close FROM PriceData WHERE stock_id = (SELECT stock_id FROM Stock WHERE symbol = %s)", (symbol,))
    data = cur.fetchall()
    conn.close()
    
    df = pd.DataFrame(data, columns=['date', 'close'])
    df['date'] = pd.to_datetime(df['date'])
    df['date_ordinal'] = df['date'].apply(lambda x: x.toordinal())  # Convert dates to numeric format
    return df

# Predict stock price using Linear Regression
def predict_stock_price(symbol):
    df = fetch_data(symbol)
    X = df[['date_ordinal']]
    y = df['close']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    model = LinearRegression()
    model.fit(X_train, y_train)
    
    future_dates = pd.date_range(start=df['date'].max(), periods=5).to_frame()
    future_dates['date_ordinal'] = future_dates[0].apply(lambda x: x.toordinal())
    
    predicted_prices = model.predict(future_dates[['date_ordinal']])
    
    return {
        "predicted_dates": future_dates[0].dt.strftime('%Y-%m-%d').tolist(),
        "predicted_prices": predicted_prices.tolist()
    }
