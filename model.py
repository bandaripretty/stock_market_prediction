engine = create_engine('postgresql://postgres:T%21m3L1n3%40Secure%232024@localhost/stock_data')

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sqlalchemy import create_engine
from sklearn.metrics import mean_squared_error, r2_score
import joblib
import os
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


# Connect to PostgreSQL database
engine = create_engine('postgresql://postgres:T%21m3L1n3%40Secure%232024@localhost/stock_data')


db = SQLAlchemy()

class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)
    
def train_model(symbol):
    try:
        # Fetch data from PostgreSQL
        query = f"SELECT open, high, low, close, volume FROM stock_prices WHERE symbol = '{symbol}'"
        df = pd.read_sql(query, engine)
        
        # Check if there is enough data
        if df.shape[0] < 100:
            print("Not enough data to train the model.")
            return None, None
        
        # Prepare the data for model training
        X = df[['open', 'high', 'low', 'volume']]
        y = df['close']
        
        # Split the data into training and testing sets
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        # Train the model
        model = LinearRegression()
        model.fit(X_train, y_train)
        
        # Predict stock prices for the test set
        predictions = model.predict(X_test)
        
        # Calculate performance metrics
        mse = mean_squared_error(y_test, predictions)
        r2 = r2_score(y_test, predictions)
        print(f"Model Performance - MSE: {mse}, R^2: {r2}")
        
        # Save the trained model to disk
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        model_filename = f"stock_model_{symbol}_{timestamp}.joblib"
        model_path = os.path.join('models', model_filename)
        os.makedirs('models', exist_ok=True)
        joblib.dump(model, model_path)
        print(f"Model trained and saved as '{model_path}'.")
        
        return model, predictions
    
    except Exception as e:
        print(f"Error occurred: {e}")
        return None, None

# Example usage
if __name__ == "__main__":
    model, predictions = train_model('AAPL')
    if predictions is not None:
        print("Predictions:", predictions)
